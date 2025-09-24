from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from PIL import Image
import pilgram
import io

router = APIRouter()


# Lista de filtros disponíveis no pilgram
AVAILABLE_FILTERS = {
    "_1977": pilgram._1977,
    "aden": pilgram.aden,
    "brannan": pilgram.brannan,
    "brooklyn": pilgram.brooklyn,
    "clarendon": pilgram.clarendon,
    "earlybird": pilgram.earlybird,
    "gingham": pilgram.gingham,
    "hudson": pilgram.hudson,
    "inkwell": pilgram.inkwell,
    "kelvin": pilgram.kelvin,
    "lark": pilgram.lark,
    "lofi": pilgram.lofi,
    "maven": pilgram.maven,
    "mayfair": pilgram.mayfair,
    "moon": pilgram.moon,
    "nashville": pilgram.nashville,
    "perpetua": pilgram.perpetua,
    "reyes": pilgram.reyes,
    "rise": pilgram.rise,
    "slumber": pilgram.slumber,
    "stinson": pilgram.stinson,
    "toaster": pilgram.toaster,
    "valencia": pilgram.valencia,
    "walden": pilgram.walden,
    "willow": pilgram.willow,
    "xpro2": pilgram.xpro2,
}


@router.post("/apply-filter/{filter_name}")
async def apply_filter(filter_name: str, file: UploadFile = File(...), quality: int = 90):

    # Verifica se o filtro existe
    if filter_name not in AVAILABLE_FILTERS:
        raise HTTPException(status_code=400, detail=f"Filtro não disponível. Filtros disponíveis: {list(AVAILABLE_FILTERS.keys())}")

    try:
        # Lê a imagem enviada
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Aplica o filtro
        filtered_image = AVAILABLE_FILTERS[filter_name](image)

        # Salva a imagem em um buffer de bytes
        output_buffer = io.BytesIO()
        filtered_image.save(output_buffer, format="JPEG", quality=quality)
        output_buffer.seek(0)

        # Retorna a imagem processada
        return Response(content=output_buffer.getvalue(), media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a imagem: {str(e)}")


@router.get("/available-filters")
async def get_available_filters():
    return {"available_filters": list(AVAILABLE_FILTERS.keys())}
