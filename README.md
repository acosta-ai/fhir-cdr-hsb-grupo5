# 🏥 Repositorio Clínico Central (FHIR CDR) con Health Service Bus (HSB)

**Grupo 5 — Sistemas Distribuidos**  
**Integrantes:** Carlos Andrés Acosta Herrera & Juan David Benítez Ruiz  
**Docente:** Ing. Jaider Enrique Reyes Herazo  
**Institución:** Corporación Universitaria Antonio José de Sucre  

---

## 📌 Descripción del Proyecto

Este proyecto implementa una arquitectura distribuida de interoperabilidad en salud basada en el estándar internacional **HL7 FHIR R4**. Resuelve el problema de la fragmentación de la información médica unificando en tiempo real historias clínicas provenientes de múltiples sedes hospitalarias independientes.

### 🏗️ Componentes de la Arquitectura

1. **Repositorio Clínico Central (CDR):**  
   Desplegado mediante **HAPI FHIR v7.2.0** en un contenedor Docker sobre el puerto `8080`, exponiendo endpoints RESTful nativos (`/Patient`, `/Observation`).
2. **Health Service Bus (HSB):**  
   Componente de mediación desarrollado en **Python** (`charla.py`) que recibe eventos clínicos de 3 sedes asistenciales (Sincelejo, Cartagena y Corozal), homologa la estructura a recursos FHIR R4, vincula las referencias de identidad y realiza la ingesta HTTP hacia el CDR.
3. **Vocabularios y Estándares Clínicos:**
   - **HL7 FHIR R4:** Recursos `Patient` y `Observation`.
   - **LOINC:** `2339-0` (Glucosa en sangre) y `8867-4` (Frecuencia cardíaca).
   - **UCUM:** Unidades de medida `mg/dL` y `/min` (latidos por minuto).
4. **Clientes Distribuidos:**  
   Consumo validado mediante **Postman** y navegador web desde nodos externos en la red.

---

## 🚀 Despliegue Rápido

### Prerrequisitos
- Docker y Docker Compose
- Python 3.8+ (con librería `requests`)

### 1. Iniciar el Servidor CDR (HAPI FHIR)
```bash
docker compose up -d
```
> *Nota: Espere entre 35 y 45 segundos mientras el servidor Java de HAPI FHIR completa su inicialización en el puerto 8080.*

### 2. Ejecutar la Ingesta Distribuida (HSB)
```bash
python3 charla.py
```
El script registrará a los pacientes y sus respectivas mediciones clínicas con confirmación en pantalla.

---

## 🔍 Consultas de Prueba (Postman / Browser)

### 1. Consultar Observaciones de Glucosa (Filtro LOINC 2339-0)
```http
GET http://localhost:8080/fhir/Observation?code=2339-0&_pretty=true
```
- **Respuesta:** `Bundle` de tipo `searchset` con `"total": 3` mediciones expresadas en `mg/dL`.

### 2. Consultar Frecuencia Cardíaca (Filtro LOINC 8867-4)
```http
GET http://localhost:8080/fhir/Observation?code=8867-4&_pretty=true
```
- **Respuesta:** `Bundle` con `"total": 2` mediciones de pulso en `bpm`.

### 3. Consultar Todo el Consolidado Clínico
```http
GET http://localhost:8080/fhir/Observation?_pretty=true
```
- **Respuesta:** Total de 5 observaciones consolidadas de todas las sedes.

### 4. Consultar Pacientes Registrados
```http
GET http://localhost:8080/fhir/Patient?_pretty=true
```

---

## 📁 Estructura del Repositorio

```text
├── docker-compose.yml   # Despliegue de HAPI FHIR Server v7.2.0
├── charla.py            # Simulador del bus de servicios (HSB)
└── README.md            # Documentación técnica de arquitectura
```
