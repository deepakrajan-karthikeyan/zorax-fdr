"""Hugging Face Space demo for ZORAX document intelligence.

The 120B model is accessed through Hugging Face Inference Providers when
HF_TOKEN is configured. Without a token, the UI remains usable in DEMO mode
and returns a transparent local extraction example.
"""

from __future__ import annotations

import base64
import json
import os
import re
from pathlib import Path
from typing import Any

import gradio as gr

MODEL_ID = "nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4"
CONFIDENCE_THRESHOLD = 0.85


def _demo_result(filename: str, prompt: str) -> dict[str, Any]:
    return {
        "mode": "DEMO_FALLBACK",
        "model": MODEL_ID,
        "document": filename or "no file supplied",
        "prompt": prompt,
        "instrumentType": "FDR",
        "referenceNumber": "SBI/FDR/824190",
        "issuingBank": "State Bank of India",
        "depositAmount": 2500000,
        "currency": "INR",
        "maturityDate": "2099-03-12",
        "confidence": 0.96,
        "requiresHumanReview": False,
        "notice": "No HF_TOKEN configured. This is synthetic demo output, not bank verification.",
    }


def _image_data(path: str) -> str:
    suffix = Path(path).suffix.lower()
    media_type = "image/png" if suffix == ".png" else "image/jpeg"
    encoded = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


def _extract_json(text: str) -> dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("The model did not return a JSON object")
    result = json.loads(match.group(0))
    result.setdefault("model", MODEL_ID)
    result.setdefault("mode", "HF_INFERENCE")
    confidence = float(result.get("confidence", 0))
    result["requiresHumanReview"] = confidence < CONFIDENCE_THRESHOLD
    return result


def parse_document(file_path: str | None, prompt: str) -> tuple[dict[str, Any], str]:
    """Parse an uploaded document or image with the configured model provider."""
    filename = Path(file_path).name if file_path else ""
    token = os.getenv("HF_TOKEN")
    if not file_path:
        return _demo_result(filename, prompt), "Upload a PDF-rendered image or a permitted image file."
    if not token:
        result = _demo_result(filename, prompt)
        return result, "DEMO mode: configure HF_TOKEN in Space secrets to call the model."

    try:
        from huggingface_hub import InferenceClient

        client = InferenceClient(api_key=token)
        instruction = (
            "Extract this financial instrument into JSON only. Use this schema: "
            '{"instrumentType":"FDR|SECURITY_DEPOSIT","referenceNumber":string,'
            '"issuingBank":string,"depositAmount":number,"currency":"INR",'
            '"maturityDate":"YYYY-MM-DD","confidence":number}. '
            f"Additional operator instruction: {prompt or 'None'}"
        )
        response = client.chat_completion(
            model=MODEL_ID,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {"type": "image_url", "image_url": {"url": _image_data(file_path)}},
                ],
            }],
            max_tokens=700,
            temperature=0.1,
        )
        result = _extract_json(response.choices[0].message.content)
        return result, "HF inference completed. Review the confidence score before saving."
    except Exception as error:
        result = _demo_result(filename, prompt)
        result["providerError"] = str(error)
        return result, "Provider call failed; showing synthetic fallback. No record was approved."


with gr.Blocks(title="ZORAX · Nemotron Document Intelligence") as demo:
    gr.Markdown(
        f"""# ZORAX · Nemotron Document Intelligence
**DEMO Space** · model adapter for [`{MODEL_ID}`](https://huggingface.co/{MODEL_ID})

Upload a rendered FDR document or image. Results are suggestions only: low-confidence
extractions must be reviewed by an authorized official and are never bank verification.
"""
    )
    with gr.Row():
        with gr.Column(scale=1):
            document = gr.File(
                label="FDR document or image",
                file_types=[".png", ".jpg", ".jpeg"],
                type="filepath",
            )
            prompt = gr.Textbox(
                label="Extraction instruction",
                value="Extract the FDR number, issuing bank, amount, and maturity date.",
            )
            run = gr.Button("Parse with Nemotron", variant="primary")
        with gr.Column(scale=1):
            output = gr.JSON(label="Structured extraction")
            status = gr.Markdown("Ready. Configure `HF_TOKEN` in Space secrets for live inference.")
    run.click(parse_document, inputs=[document, prompt], outputs=[output, status])
    gr.Markdown(
        "**Security note:** files are untrusted input. This demo does not persist uploads, "
        "does not create signed download URLs, and does not represent an official AICTE or bank integration."
    )


if __name__ == "__main__":
    demo.launch()
