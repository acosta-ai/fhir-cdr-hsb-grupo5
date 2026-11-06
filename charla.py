"""
charla.py - Health Service Bus (HSB) & Repositorio Clínico Central (CDR)
Grupo 5 - Sistemas Distribuidos
Integrantes: Carlos Andrés Acosta Herrera & Juan David Benítez Ruiz
Docente: Ing. Jaider Enrique Reyes Herazo

Este script actúa como el mediador (HSB), recibiendo eventos clínicos
provenientes de tres sedes distintas (Sincelejo, Cartagena, Corozal),
homologándolos al estándar internacional HL7 FHIR R4 (JSON) con terminologías
LOINC y UCUM, y transmitiéndolos hacia el CDR (HAPI FHIR) vía HTTP POST.
"""

import requests
import json
import time

FHIR_BASE_URL = "http://localhost:8080/fhir"
HEADERS = {"Content-Type": "application/fhir+json"}

pacientes_sedes = [
    {
        "nombre": "Carlos",
        "apellido": "Acosta",
        "origen": "Clínica Sincelejo",
        "glucosa": 95,
        "fc": 72
    },
    {
        "nombre": "Juan",
        "apellido": "Benítez",
        "origen": "Hospital Cartagena",
        "glucosa": 110,
        "fc": 80
    },
    {
        "nombre": "Jaider",
        "apellido": "Reyes",
        "origen": "Laboratorio Corozal",
        "glucosa": 88,
        "fc": 75
    }
]

def main():
    print("=" * 65)
    print("🏥 HEALTH SERVICE BUS (HSB) -> INGESTA DISTRIBUIDA HACIA EL CDR")
    print(f"📡 Conectando a HAPI FHIR Server: {FHIR_BASE_URL}")
    print("=" * 65)

    created_patients = []

    # 1. Registro de Pacientes (Patient Resource)
    for p in pacientes_sedes:
        patient_resource = {
            "resourceType": "Patient",
            "name": [{
                "family": p["apellido"],
                "given": [p["nombre"]]
            }],
            "managingOrganization": {
                "display": p["origen"]
            }
        }
        
        try:
            res = requests.post(f"{FHIR_BASE_URL}/Patient", json=patient_resource, headers=HEADERS)
            if res.status_code in [200, 201]:
                pid = res.json().get("id")
                created_patients.append((pid, p))
                print(f"✅ [HSB] Paciente {p['nombre']} {p['apellido']} registrado exitosamente (Origen: {p['origen']}) -> ID FHIR: {pid}")
            else:
                print(f"❌ Error al registrar {p['nombre']}: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"❌ Error de conexión al CDR: {e}")
            return

    time.sleep(1)
    print("\n" + "-" * 65)
    print("🔬 ENVIANDO OBSERVACIONES CLÍNICAS (LOINC 2339-0 & 8867-4)")
    print("-" * 65)

    # 2. Registro de Observaciones (Observation Resource)
    for pid, p in created_patients:
        # A. Glucosa en sangre (LOINC 2339-0, Unidad UCUM mg/dL)
        obs_glucose = {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "2339-0",
                    "display": "Glucose [Mass/volume] in Blood"
                }]
            },
            "subject": {"reference": f"Patient/{pid}"},
            "valueQuantity": {
                "value": p["glucosa"],
                "unit": "mg/dL",
                "system": "http://unitsofmeasure.org",
                "code": "mg/dL"
            }
        }
        rg = requests.post(f"{FHIR_BASE_URL}/Observation", json=obs_glucose, headers=HEADERS)
        print(f"  🩸 [Glucosa LOINC 2339-0] {p['nombre']} = {p['glucosa']} mg/dL (Status: {rg.status_code} OK)")

        # B. Frecuencia Cardíaca (LOINC 8867-4, Unidad UCUM /min)
        obs_hr = {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "8867-4",
                    "display": "Heart rate"
                }]
            },
            "subject": {"reference": f"Patient/{pid}"},
            "valueQuantity": {
                "value": p["fc"],
                "unit": "/min",
                "system": "http://unitsofmeasure.org",
                "code": "/min"
            }
        }
        rh = requests.post(f"{FHIR_BASE_URL}/Observation", json=obs_hr, headers=HEADERS)
        print(f"  💓 [Frec. Cardíaca LOINC 8867-4] {p['nombre']} = {p['fc']} bpm (Status: {rh.status_code} OK)")

    print("\n" + "=" * 65)
    print("🎉 INGESTA COMPLETADA EXITOSAMENTE")
    print("El Repositorio Clínico (CDR) está listo para consultas distribuidas.")
    print("=" * 65)

if __name__ == "__main__":
    main()
