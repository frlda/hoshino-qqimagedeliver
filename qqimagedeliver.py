from hoshino import Service, get_bot
from hoshino.typing import CQEvent
from nonebot import MessageSegment, on_startup
from quart import Quart, request, jsonify
import asyncio
import logging

#去除心跳提醒
class HeartbeatFilter(logging.Filter):
    def filter(self, record):
        return "received event: meta_event.heartbeat" not in record.getMessage()


root_logger = logging.getLogger()
root_logger.addFilter(HeartbeatFilter())
root_logger.setLevel(logging.INFO)


logger = logging.getLogger('qqimagedeliver')
logger.setLevel(logging.INFO)

sv = Service('qqimagedeliver', help_='接收并处理POST请求，发送消息和图片到QQ好友或群')

app = Quart(__name__)

@app.route('/', methods=['POST'])
async def handle_post():
    try:
        raw_data = await request.get_data()
        logger.info(f"Raw request data: {raw_data}")
        logger.info(f"Request headers: {request.headers}")

        data = await request.form

        logger.info(f"Parsed data: {data}")

        if not data:
            return jsonify({"error": "No data received"}), 400

        to = data.get('to')
        info = data.get('info')
        image_b64 = data.get('image')

        if not to or not info:
            return jsonify({"error": "Missing 'to' or 'info' in the request"}), 400

        result = await handle_qqimagedeliver_request(to, info, image_b64)
        logger.info(f"Request handled with result: {result}")
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in handle_post: {str(e)}")
        return jsonify({"error": str(e)}), 500

async def handle_qqimagedeliver_request(to, info, image_b64=None):
    try:
        bot = get_bot()
        msg = info
        if image_b64:
            msg += MessageSegment.image(f"base64://{image_b64}")
        
        if to.startswith('g'):
            group_id = int(to[1:])
            await bot.send_group_msg(group_id=group_id, message=msg)
            logger.info(f"Message sent to group {group_id}: {info}")
        else:
            user_id = int(to)
            await bot.send_private_msg(user_id=user_id, message=msg)
            logger.info(f"Message sent to user {user_id}: {info}")
        
        return {"success": True, "message": "Message sent successfully"}
    except Exception as e:
        logger.error(f"Error in handle_qqimagedeliver_request: {str(e)}")
        return {"error": str(e)}

@sv.on_fullmatch('测试qqimagedeliver')
async def test_qqimagedeliver(bot, ev: CQEvent):
    await bot.send(ev, "qqimagedeliver插件正在运行，监听端口：8888")

async def run_server():
    config = {"host": "0.0.0.0", "port": 8888}
    logger.info(f"Starting qqimagedeliver server on {config['host']}:{config['port']}")
    await app.run_task(**config)

@on_startup
async def startup():
    asyncio.create_task(run_server())
    logger.info('qqimagedeliver插件已初始化并在端口8888上启动')


startup()
