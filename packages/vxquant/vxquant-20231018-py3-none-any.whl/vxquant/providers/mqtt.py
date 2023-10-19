"""基于MQTT的数据发布/订阅服务"""
from secrets import token_hex
from typing import Any, Union
from pathlib import Path
from paho.mqtt.client import Client as MQTTClient
from vxquant.providers.base import vxPublisher, vxSubscriber
from vxutils.sched.core import vxScheduler, vxTrigger, vxsched, vxEvent
from vxutils import logger, vxtime

__clients__ = {}
__MQTTIDENTY__ = "vxquant"


def mqttclient_builder(
    client_id: str = "",
    broker: str = "broker.emqx.io",
    port: int = 1883,
    ca_certs: Union[Path, str] = None,
    username: str = "",
    passwd: str = "",
) -> MQTTClient:
    global __clients__

    client_id = client_id or f"vxquant_{token_hex(16)}"
    if client_id not in __clients__:
        client = MQTTClient(client_id=client_id, userdata=__MQTTIDENTY__)

        if ca_certs:
            client.tls_set(ca_certs=str(ca_certs))

        if username and passwd:
            client.username_pw_set(username=username, password=passwd)

        client.connect(broker, port)
        client.loop_start()
        vxtime.sleep(1)
        __clients__[client_id] = client
    return __clients__[client_id]


class vxMQTTPublisher(vxPublisher):
    def set_context(self, context, **kwargs):
        super().set_context(context=context, **kwargs)

        if "mqtt_client" not in context:
            context.mqtt_client = mqttclient_builder()

    def __call__(
        self,
        event: str | vxEvent,
        data: Any = None,
        trigger: vxTrigger = None,
        priority: int = 10,
        **kwargs,
    ) -> None:
        if isinstance(event, str):
            t_event = vxEvent(
                type=str(event), data=data, trigger=trigger, priority=priority, **kwargs
            )
        elif isinstance(event, vxEvent):
            t_event = event
        else:
            raise ValueError(f"仅支持发布vxEvent / str类型的消息 {type(event)}")

        topics = f"{__MQTTIDENTY__}/{t_event.type}"
        if t_event.channel:
            topics += f"/{t_event.channel}"

        logger.info("发布消息: %s", topics)
        self.context.mqtt_client.publish(topics, t_event.dumps())


class vxMQTTSubscriber(vxSubscriber):
    def set_context(self, context, **kwargs):
        super().set_context(context=context, **kwargs)

        if "mqtt_client" not in context:
            self.context.mqtt_client = mqttclient_builder()

        self.context.mqtt_client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        if userdata == __MQTTIDENTY__:
            t_event = vxEvent.loads(pickle_obj=msg.payload)
            vxsched.submit_event(t_event)
        else:
            logger.warning(f"未知的MQTT消息来源 {userdata}")

    def __call__(self, event_type: str, channel: str = None) -> None:
        if not channel:
            channel = "#"
        topcis = f"{__MQTTIDENTY__}/{event_type}/{channel}"
        self.context.mqtt_client.subscribe(topcis)
        logger.warning("订阅: %s", topcis)


@vxsched.register("test")
def test(context, event):
    logger.info("收到远程消息: %s", event)


if __name__ == "__main__":
    from vxutils.sched.core import vxContext

    context = vxContext()
    mqtt_client = mqttclient_builder(
        "test",
        "rde84dd4.ala.cn-hangzhou.emqxsl.cn",
        8883,
        "/mnt/d/quant/dist/emqxsl-ca.crt",
        "test",
        "123456",
    )
    vxsched.start()

    publisher = vxMQTTPublisher()
    subscriber = vxMQTTSubscriber()
    publisher.set_context(context, mqtt_client=mqtt_client)
    subscriber.set_context(context, mqtt_client=mqtt_client)
    subscriber("test", "1234")
    publisher("test", "123", channel="1234")
    vxtime.sleep(10)
    vxsched.stop()
    # client.loop_stop()
