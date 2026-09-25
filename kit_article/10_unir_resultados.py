import json

VALIDATION_FILE = "data/llm_results_validation.json"

REMAINING_FILE = "data/llm_results_remaining.json"

OUTPUT_FILE = "data/llm_results.json"


with open(VALIDATION_FILE, encoding="utf8") as f:
    validation = json.load(f)

with open(REMAINING_FILE, encoding="utf8") as f:
    remaining = json.load(f)

resultado = validation + remaining

# Ordena por repositório e número da PR
resultado.sort(
    key=lambda x: (
        x["repo"],
        x["pr_number"]
    )
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf8"
) as f:

    json.dump(
        resultado,
        f,
        indent=2,
        ensure_ascii=False
    )

print()

print("=" * 60)
print("RESULTADOS UNIFICADOS")
print("=" * 60)

print(f"Validação : {len(validation)}")
print(f"Restantes : {len(remaining)}")
print(f"Total     : {len(resultado)}")

# Verifica duplicatas
ids = [

    (
        pr["repo"],
        pr["pr_number"]
    )

    for pr in resultado

]

duplicados = len(ids) - len(set(ids))

print(f"Duplicados: {duplicados}")

print("=" * 60)

if len(resultado) == 1152 and duplicados == 0:

    print("\n✓ Arquivo final criado com sucesso.")

else:

    print("\n⚠ Verifique o arquivo gerado.")