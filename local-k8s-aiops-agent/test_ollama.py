from llm import analyze
print(analyze('{"pod":"backend-test","ready":false,"last_termination_reason":"OOMKilled","restart_count":4}'))
