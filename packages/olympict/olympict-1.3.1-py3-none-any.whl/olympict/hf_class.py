from typing import Optional

import transformers
import huggingface_hub

from olympict.files.o_image import OlympImage


class HuggingFaceModel:
    def __init__(
        self,
        hf_id: str,
        revision: Optional[str] = None,
        huggingface_token: Optional[str] = None,
    ) -> None:
        infos = huggingface_hub.model_info(
            hf_id, revision=revision, token=huggingface_token
        )

        self.model_constructor = getattr(
            transformers, infos.transformersInfo["auto_model"]
        )
        self.processor_constructor = getattr(
            transformers, infos.transformersInfo["processor"]
        )

        self.model = self.model_constructor.from_pretrained(hf_id)
        self.processor = self.processor_constructor.from_pretrained(hf_id)

    def infer(self, o: OlympImage) -> OlympImage:
        # Pillow format
        inputs = self.processor(images=[o.img[:, :, ::-1]], return_tensors="pt")

        outputs = self.model(**inputs)
        logits = outputs.logits

        # model predicts one of the 1000 ImageNet classes
        label_id = logits.argmax(-1).item()

        o.metadata["label"] = self.model.config.id2label[label_id]
        o.metadata["label_id"] = label_id

        return o
