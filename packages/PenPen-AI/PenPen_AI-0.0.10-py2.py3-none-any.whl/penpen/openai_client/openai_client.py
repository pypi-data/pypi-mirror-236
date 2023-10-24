from __future__ import annotations
from enum import Enum
import json
import time
from typing import Any, Callable, Dict, Generator, List, Optional, Union, cast
import openai
import tiktoken
import os
from .openai_client_exceptions import (
    MissingOpenaiAPIKeyException,
    MaxConsecutiveFunctionCallsExceeded,
    FunctionCallbackNotProvided,
)
import random

supported_models = ["gpt-3.5-turbo-0613", "gpt-3-5-turbo-16k-0613", "gpt-4-0613"]


class GPTModel(Enum):
    """
    The OPENAI GPT models available.
    Only those that support functions are listed, so just:
    gpt-3.5-turbo-0613, gpt-3-5-turbo-16k-0613, gpt-4-0613
    """

    GPT_3_5_TURBO = ("gpt-3.5-turbo-0613", 4096, 0.0015, 0.002)
    GPT_3_5_TURBO_16K = ("gpt-3.5-turbo-16k-0613", 16384, 0.003, 0.004)
    GPT_4 = ("gpt-4-0613", 8192, 0.03, 0.06)

    @staticmethod
    def from_string(string: str) -> GPTModel:
        for model in GPTModel:
            if model.string == string:
                return model
        raise Exception(f"Model {string} not supported")

    def __init__(self, string, max_tokens, price_1k_tokens_in, price_1k_tokens_out):
        self.string = string
        self.max_tokens = max_tokens
        self.price_1k_tokens_in = price_1k_tokens_in
        self.price_1k_tokens_out = price_1k_tokens_out

    def __str__(self):
        return self.string


class JobTokensExpense:
    """
    Tracks the number of tokens spent on a job and on which GPTModel.
    """

    def __init__(
        self,
        gpt_model: GPTModel,
        prompt_tokens=0,
        completion_tokens=0,
        total_tokens=0,
        rough_estimate=False,
    ):
        self.gpt_model = gpt_model
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens
        self.rough_estimate = rough_estimate

    @staticmethod
    def from_openai_usage_dictionary(
        gpt_model: GPTModel, dictionary: dict
    ) -> JobTokensExpense:
        return JobTokensExpense(
            gpt_model=gpt_model,
            prompt_tokens=dictionary["prompt_tokens"],
            completion_tokens=dictionary["completion_tokens"],
            total_tokens=dictionary["total_tokens"],
        )

    def spend(self, prompt_tokens, completion_tokens, total_tokens):
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.total_tokens += total_tokens

    def add_from(self, other_expense: JobTokensExpense):
        self.prompt_tokens += other_expense.prompt_tokens
        self.completion_tokens += other_expense.completion_tokens
        self.total_tokens += other_expense.total_tokens
        if other_expense.rough_estimate:
            self.rough_estimate = True  # becomes rough if summed with something rough

    def get_cost(self):
        return (self.prompt_tokens / 1000) * self.gpt_model.price_1k_tokens_in + (
            self.completion_tokens / 1000
        ) * self.gpt_model.price_1k_tokens_out

    def __str__(self):
        string_repr = (
            f"GPT model: {self.gpt_model}\n"
            f"Prompt tokens: {self.prompt_tokens}\n"
            f"Completion tokens: {self.completion_tokens}\n"
            f"Total tokens: {self.total_tokens}\n"
            f"Cost: {round(self.get_cost(),4)}$"
        )

        if self.rough_estimate:
            string_repr += "\n(warning: rough estimate)"

        return string_repr

    def to_json(self):
        return {
            "model": self.gpt_model.string,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "cost": self.get_cost(),
            "rough_estimate": self.rough_estimate,
        }


def estimate_token_count(string: str, model: GPTModel) -> int:
    """Returns the number of tokens in a text string."""

    model_name = model.string
    model_name = model_name.replace("-0613", "")
    model_name = model_name.replace("-16k", "")

    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# private class used to store a call context when looping happens because of function
class OpenaiCallContext:
    def __init__(
        self,
        messages: List[dict],
        call_kwargs: OpenAICallKwargs,
        iterations: int = 0,
    ):
        self.messages = messages
        self.call_kwargs = call_kwargs
        self.iterations = iterations


class OpenAICallKwargs:
    """
    Model class to conveniently store the call kwargs for an OpenAI call.
    """

    def __init__(
        self,
        model: GPTModel = GPTModel.GPT_3_5_TURBO,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        temperature: float = 0.0,
        top_p: Optional[int] = None,
        n: int = 1,
        function_call: Optional[Union[str, Dict]] = None,
        functions: Optional[List[Dict[str, Any]]] = None,
        function_callback: Optional[Callable[[str, Dict[str, Any]], Any]] = None,
        max_consecutive_function_calls: int = 5,
        max_retries_after_openai_error: int = 15,
        retry_delay_seconds: int = 10,
        exponential_base: int = 2,
        exponential_delay: int = 1,
        exponential_cap: Optional[int] = None,
        jitter: bool = True,
        function_call_debug_stream=False,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.stream = stream
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.function_call = function_call
        self.functions = functions
        self.function_callback = function_callback
        self.max_consecutive_function_calls = max_consecutive_function_calls
        self.max_retries_after_openai_error = max_retries_after_openai_error
        self.retry_delay_seconds = retry_delay_seconds
        self.exponential_base = exponential_base
        self.exponential_delay = exponential_delay
        self.exponential_cap = exponential_cap
        self.jitter = jitter
        self.function_call_debug_stream = function_call_debug_stream

    def to_openai_kwargs(self) -> dict:
        """
        returns the dictionary formatted for an openai call using the official openai client.
        """
        kwargs = {
            "model": self.model.string,
            "temperature": self.temperature,
            "stream": self.stream,
            "n": self.n,
        }

        if self.max_tokens is not None:
            kwargs["max_tokens"] = self.max_tokens

        if self.top_p is not None:
            kwargs["top_p"] = self.top_p

        if self.functions is not None:
            if self.function_call is None:
                kwargs["function_call"] = "auto"
            else:
                kwargs["function_call"] = self.function_call

            kwargs["functions"] = self.functions

        return kwargs


class ErrorHandlingMethod(Enum):
    FAIL = "fail"
    RETRY = "retry"
    EXPONENTIAL_BACKOFF = "exponential_backoff"


class OpenAIClient:
    """
    A simple openai wrapper client, that gets initialized with basic openai parameters and offers
    function calls support.

    Attributes
    ----------
        openai_call_kwargs : OpenAICallKwargs
            the kwargs that will be passed to the openai call, can be overridden for single specific calls
            if needed with the call_openai method.
        functions : list
            the list of functions that will be called by the client
        max_consecutive_function_calls: int
            the maximum number of consecutive function calls that can be made by the agent, defaults to 5
            for safety reasons, to avoid unwanted loops that might impact up token usage
        openai_api_key: str
            the openai api key, defaults to the OPENAI_API_KEY environment variable if not provided

    Methods
    -------
        call_openai(messages, openai_call_kwargs)
            performs the call to OpenAI and returns the response and the expense


    Raises
    ------
        MissingOpenaiAPIKeyException
            if the OPENAI_API_KEY environment variable is not set and no api key is provided
    """

    def __init__(
        self,
        openai_call_kwargs: Optional[OpenAICallKwargs] = None,
        openai_api_key: Optional[str] = None,
    ):
        openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise MissingOpenaiAPIKeyException()
        openai.api_key = openai_api_key

        self.openai_call_kwargs = openai_call_kwargs or OpenAICallKwargs()

        self.__expense = {
            GPTModel.GPT_3_5_TURBO.string: JobTokensExpense(
                gpt_model=GPTModel.GPT_3_5_TURBO
            ),
            GPTModel.GPT_3_5_TURBO_16K.string: JobTokensExpense(
                gpt_model=GPTModel.GPT_3_5_TURBO_16K
            ),
            GPTModel.GPT_4.string: JobTokensExpense(gpt_model=GPTModel.GPT_4),
        }

    @staticmethod
    def __handle_openai_error(error: openai.OpenAIError) -> ErrorHandlingMethod:
        # errors are handled according to the guidelines here: https://platform.openai.com/docs/guides/error-codes/api-errors (dated 03/10/2023)
        # this map indexes all the error that require a retry or an exponential backoff, every other error is a fail
        error_handling_map = {
            openai.error.RateLimitError: ErrorHandlingMethod.EXPONENTIAL_BACKOFF,
            openai.error.ServiceUnavailableError: ErrorHandlingMethod.EXPONENTIAL_BACKOFF,
            openai.error.APIError: ErrorHandlingMethod.RETRY,
            openai.error.TryAgain: ErrorHandlingMethod.RETRY,
            openai.error.Timeout: ErrorHandlingMethod.RETRY,
            openai.error.APIConnectionError: ErrorHandlingMethod.RETRY,
        }

        for error_type, error_handling_method in error_handling_map.items():
            if isinstance(error, error_type):
                return error_handling_method

        return ErrorHandlingMethod.FAIL

    def get_openai_response(
        self,
        messages: List[dict],
        override_openai_kwargs: Optional[OpenAICallKwargs] = None,
    ) -> Union[str, Generator[str, None, None]]:
        """
        Calls OpenAI with the passed parameters and returns or streams the response.

        Parameters
        ----------
            messages : list
                the list of messages to be sent
            override_openai_kwargs : OpenAICallKwargs (optional)
                if provided, overrides the openai call kwargs for this specific call with the provided ones
        Returns
        -------
            the response of the openai call
                the response object
        """

        kwargs = override_openai_kwargs or self.openai_call_kwargs

        if kwargs.functions is not None and kwargs.function_callback is None:
            raise FunctionCallbackNotProvided()

        call_context = OpenaiCallContext(messages, kwargs)

        return self.__call_openai(call_context)

    def __call_openai(
        self, call_context: OpenaiCallContext
    ) -> Union[str, Generator[str, None, None]]:
        call_context.iterations += 1
        if (
            call_context.iterations
            > call_context.call_kwargs.max_consecutive_function_calls
        ):
            raise MaxConsecutiveFunctionCallsExceeded(
                f"PenPen OpenAI Client Max consecutive function calls exceeded ({call_context.call_kwargs.max_consecutive_function_calls})"
            )

        formatted_kwargs = call_context.call_kwargs.to_openai_kwargs()
        formatted_kwargs["messages"] = call_context.messages
        delay = call_context.call_kwargs.exponential_delay

        retries = 0
        while retries < call_context.call_kwargs.max_retries_after_openai_error:
            try:
                response = openai.ChatCompletion.create(**formatted_kwargs)

                if call_context.call_kwargs.stream:
                    return self.__process_openai_stream_response(response, call_context)
                else:
                    return self.__process_openai_response(response, call_context)

            except openai.OpenAIError as error:
                error_handling_method = OpenAIClient.__handle_openai_error(error)

                if error_handling_method == ErrorHandlingMethod.FAIL:
                    raise Exception(f"PenPen OpenAI Client error: {error}")

                sleep_time = call_context.call_kwargs.retry_delay_seconds
                if error_handling_method == ErrorHandlingMethod.RETRY:
                    print(
                        f"PenPen OpenAI Client error ({error.code}): {error}. Retrying in {sleep_time} seconds..."
                    )
                elif error_handling_method == ErrorHandlingMethod.EXPONENTIAL_BACKOFF:
                    if (
                        call_context.call_kwargs.exponential_cap is not None
                        and delay > call_context.call_kwargs.exponential_cap
                    ):
                        delay = call_context.call_kwargs.exponential_cap
                    else:
                        delay *= call_context.call_kwargs.exponential_base

                    jitter = 1 + call_context.call_kwargs.jitter * random.random()
                    delay *= jitter

                    sleep_time = delay
                    print(
                        f"PenPen OpenAI Client error ({error.code}): {error}. Performing Exponential backoff, retrying in {sleep_time} seconds..."
                    )

                time.sleep(sleep_time)
                retries += 1

            except json.decoder.JSONDecodeError as e:
                print(
                    f"PenPen OpenAI Client error failed on jsondecode, probably context too big and LLM unable to complete the request."
                )
                raise e

            except Exception as e:
                print(
                    f"PenPen OpenAI Client error: {e}. Retrying in {call_context.call_kwargs.retry_delay_seconds} seconds..."
                )
                time.sleep(call_context.call_kwargs.retry_delay_seconds)
                retries += 1

        raise Exception(
            f"PenPen OpenAI Client Max retries exceeded! OpenAI API call failed {call_context.call_kwargs.max_retries_after_openai_error} times."
        )

    def __process_openai_stream_response(
        self, response: Any, call_context: OpenaiCallContext
    ) -> Generator[str, None, None]:
        # the streaming response received as response_delta chunks by the generator returned by the openai api
        # is accumulated and yielded at the same time, this is because we need to check if there is a function
        # to be called.
        received_message = {}
        for response_delta in response:
            if len(response_delta["choices"]) > 0:
                # check content exists
                message_delta = response_delta["choices"][0]["delta"]
                # merge the new delta into the accumulated one

                if (
                    call_context.call_kwargs.function_call_debug_stream
                    and "function_call" in message_delta
                ):
                    print(
                        message_delta["function_call"]["arguments"], end="", flush=True
                    )

                received_message = OpenAIClient.__merge_message_deltas(
                    received_message, message_delta
                )

                # if there is some content in the message delta, yield it
                # this means that openai is not calling a function and is streaming some content
                if "content" in message_delta and message_delta["content"] is not None:
                    yield response_delta["choices"][0]["delta"]["content"]

                # check if there is a finsh reason, meaning that openai has completed streaming
                # and process the accumulated response
                if response_delta["choices"][0]["finish_reason"] is not None:
                    # log token expense
                    self.__log_rough_expense_from_streaming_response(
                        received_message, call_context
                    )

                    # handle the final accumulated response message, checking if there is a function to be called
                    # or the srteam is finished
                    yield from self.__handle_response_message(
                        received_message, call_context
                    )

    def __process_openai_response(self, response: Any, call_context: OpenaiCallContext):
        if len(response["choices"]) == 0:
            return ""

        # log token expense
        expense = JobTokensExpense.from_openai_usage_dictionary(
            call_context.call_kwargs.model, response["usage"]
        )
        self.__log_new_expense(expense)

        message = response["choices"][0]["message"]
        return self.__handle_response_message(message, call_context)

    def __handle_response_message(self, message, call_context: OpenaiCallContext):
        # must handle a function call
        if "function_call" in message:
            # cast the callback so that type checker doesn't complain
            # (null value already handled with exception in get_openai_response )
            callback = cast(
                Callable[[str, Dict[str, Any]], Dict[str, Any]],
                call_context.call_kwargs.function_callback,
            )

            # get function args and call the callback to obtain result
            function_name = message["function_call"]["name"]
            function_args = json.loads(message["function_call"]["arguments"])
            function_result = callback(function_name, function_args)

            # if the function call is auto, build the messages and call openai again passing the results
            # if function call is not set to auto but with the usual {"name":"function_name"}, passing
            # the result back to openai will cause openai to call the function again endlessly.
            # So we call openai again if and only if the function call is set to auto.
            if call_context.call_kwargs.function_call == "auto":
                new_messages = OpenAIClient.__build_messages_from_function_result(
                    message, function_result
                )
                call_context.messages.extend(new_messages)
                return self.__call_openai(call_context)

        # if the message was streaming, return a last empty string to signal the end of the stream
        # (since previous deltas have already been yielded).
        if call_context.call_kwargs.stream:
            return ""

        # if the message was not streaming, return the message content.
        return message["content"]

    def __log_rough_expense_from_streaming_response(
        self, received_message: Any, call_context: OpenaiCallContext
    ):
        sent_prompt_tokens = estimate_token_count(
            json.dumps(call_context.messages),
            model=call_context.call_kwargs.model,
        )
        received_message_tokens = estimate_token_count(
            json.dumps(received_message),
            model=call_context.call_kwargs.model,
        )
        total_tokens = sent_prompt_tokens + received_message_tokens
        rough_expense = JobTokensExpense(
            gpt_model=call_context.call_kwargs.model,
            prompt_tokens=sent_prompt_tokens,
            completion_tokens=received_message_tokens,
            total_tokens=total_tokens,
            rough_estimate=True,
        )
        self.__log_new_expense(rough_expense)

    def __log_new_expense(self, expense: JobTokensExpense):
        self.__expense[expense.gpt_model.string].add_from(expense)

    def get_expenses(self):
        """
        Returns the tokens spent in the current session in an array, one for each model.
        """
        return [
            expense for expense in self.__expense.values() if expense.total_tokens > 0
        ]

    @staticmethod
    def __merge_message_deltas(current: dict, delta: dict) -> dict:
        """Merges new delta into the accumulated one."""
        for key, value in delta.items():
            if key in current:
                if isinstance(value, str):
                    current[key] += value
                elif isinstance(value, dict):
                    current[key] = OpenAIClient.__merge_message_deltas(
                        current.get(key, {}), value
                    )
            else:
                current[key] = value

        return current

    @staticmethod
    def __build_messages_from_function_result(function_call_message, function_result):
        parsed_message_function_call = {
            k: v
            for k, v in function_call_message.items()
            if k in {"role", "content", "name"}
        }
        parsed_message_function_call["function_call"] = {
            "name": function_call_message["function_call"]["name"],
            "arguments": function_call_message["function_call"]["arguments"],
        }

        parsed_message_function_result = {
            "role": "function",
            "name": function_call_message["function_call"]["name"],
            "content": str(function_result),
        }

        return [parsed_message_function_call, parsed_message_function_result]
