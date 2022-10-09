import uuid
import time
import sys
import json
import logging
from fastapi import Response
from .oauth2 import get_token_email
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta

logger = logging.getLogger("json_log")

logging.basicConfig(level="INFO", stream=sys.stdout, format="%(message)s")


async def set_body(request, body):
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request):
    body = await request.body()
    await set_body(request, body)
    return body


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = uuid.uuid4()
        ip = (
            request.headers["x-forwarded-for"]
            if "x-forwarded-for" in request.headers.keys()
            else request.client.host
        )
        client_ip = ip.split(",")[0] if "," in ip else ip
        cookies = request.cookies
        start = time.time()
        time_format = "%Y/%m/%d %H:%M:%S"
        datetimeUTC = (datetime.utcnow().strftime(time_format),)
        datetimeKST = ((datetime.utcnow() + timedelta(hours=9)).strftime(time_format),)
        user_email = None
        query_strings = str(request.query_params)
        headers = dict(
            [
                header
                for header in zip(request.headers.keys(), request.headers.values())
                if header[0] != "authorization"
            ]
        )

        await set_body(request, await request.body())

        request_body = await get_body(request)

        request_body = request_body.decode("UTF-8")

        try:
            if "authorization" in request.headers.keys():
                token = request.headers["authorization"]
                user_email = get_token_email(token)

            response = await call_next(request)
        except Exception as error:
            error_log = {
                "datetimeUTC": f"{datetimeUTC[0]}",
                "datetimeKST": f"{datetimeKST[0]}",
                "log_level": "ERROR",
                "request_id": f"{request_id}",
                "request_method": f"{request.method}",
                "request_url": f"{request.url}",
                "request_hostname": f"{request.url.hostname}",
                "request_path": f"{request.url.path}",
                "client_ip": f"{client_ip}",
                "error_message": f"{error}",
                "user_email": f"{user_email}",
                "query_strings": f"{query_strings}"
            }

            error_log = json.dumps(error_log, indent=4)

            logger.error(error_log)

            response_dict = {
                "message": "Internal Server Error",
                "request_id": f"{request_id}",
            }

            return Response(content=f"{response_dict}", status_code=500)

        t = time.time() - start
        processedTime = str(round(t * 1000, 5)) + "ms"
        response_body = b""

        async for chunk in response.body_iterator:
            response_body += chunk

        response_body = response_body.decode("utf-8")

        info_log = {
            "datetimeUTC": f"{datetimeUTC[0]}",
            "datetimeKST": f"{datetimeKST[0]}",
            "log_level": "INFO",
            "request_id": f"{request_id}",
            "request_method": f"{request.method}",
            "request_url": f"{request.url}",
            "request_hostname": f"{request.url.hostname}",
            "request_path": f"{request.url.path}",
            "client_ip": f"{client_ip}",
            "request_headers": f"{headers}",
            "request_cookies": f"{cookies}",
            "processed_time": f"{processedTime}",
            "response_status_code": f"{response.status_code}",
            "user_email": f"{user_email}",
            "query_strings": f"{query_strings}"
        }
        if request.url.path == "/login":
            info_log["response_body"] = "{message : access token is not logged}"
            info_log["request_body"] = "{message : login is not logged}"
        else:
            info_log["response_body"] = response_body
            info_log["request_body"] = request_body

        info_log = json.dumps(info_log, indent=4)

        logger.info(info_log)

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
