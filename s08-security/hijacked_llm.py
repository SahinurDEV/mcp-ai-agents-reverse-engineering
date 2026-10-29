"""hijacked_llm.py: a fake OpenAI-compatible model that ALWAYS obeys the injection.
It simulates the worst case (a fully hijacked model) so we can test client-side controls.
Run: python3 hijacked_llm.py &   then LLM_BASE_URL=http://localhost:11500/v1 python3 agent.py ..."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        last = body["messages"][-1]
        if last["role"] == "tool":                       # after any tool result: report "success"
            msg = {"role": "assistant", "content": "Done. Everything is fine."}
        else:                                            # first turn: do what the injected note says
            msg = {"role": "assistant", "content": None, "tool_calls": [{
                "id": "call_1", "type": "function",
                "function": {"name": "notes_create",
                             "arguments": json.dumps({"title": "pwned", "body": "injected"})}}]}
        data = json.dumps({"choices": [{"message": msg, "finish_reason": "stop"}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):                        # keep the terminal quiet
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 11500), Handler).serve_forever()
