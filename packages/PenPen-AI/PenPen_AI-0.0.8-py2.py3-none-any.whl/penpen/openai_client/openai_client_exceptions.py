class MissingOpenaiAPIKeyException(Exception):
    def __init__(self):
        message = "Missing OPENAI_API_KEY, set environment variable OPENAI_API_KEY or pass it as a parameter to the agent constructor."
        super().__init__(message)


class OpenAIErrorException(Exception):
    def __init__(self, message, openai_error):
        super().__init__(message)
        self.openai_error = openai_error


class MaxConsecutiveFunctionCallsExceeded(Exception):
    def __init__(self, max_consecutive_calls):
        message = f"Max consecutive function calls exceeded: {max_consecutive_calls}"
        super().__init__(message)


class FunctionCallbackNotProvided(Exception):
    def __init__(self):
        message = "Functions passed but function callback handler has not been provided"
        super().__init__(message)
