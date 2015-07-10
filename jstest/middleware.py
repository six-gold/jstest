# coding=utf-8
from log.logger import Logger


class ResponseErrorLog(object):
    """
    logging response code/timeout and request url when the response code is not 200
    """

    def process_response(self, request, response, spider):
        Logger.log({"response_status": response.status, "url": response.url}, "response")
        return response
