# Appointment Service: API Test Specifications

## Overview
This document outlines the test cases required for the initial development of the Appointment Service API. These tests follow a TDD (Test-Driven Development) approach, targeting a Flask implementation with a PostgreSQL backend.

## Test Suite: Provider Management

### 1. List All Providers
**Endpoint:** `GET /providers`

| Scenario | Database State | Expected Status | Expected Payload |
| :--- | :--- | :--- | :--- |
| Success - Populated | 2+ provider records exist | `200 OK` | Array of objects: `[{"id": int, "name": str, "specialty": str}]` |
| Success - Empty | No records in `providers` table | `200 OK` | Empty array: `[]` |

---

## Test Suite: Availability Management

### 2. Get Provider Availability
**Endpoint:** `GET /providers/<string:name>/availability`

| Scenario | Input / Context | Expected Status | Expected Payload |
| :--- | :--- | :--- | :--- |
| **Success** | Name exists; active slots available | `200 OK` | Array of ISO-8601 strings: `["2025-10-20T09:00:00", ...]` |
| **No Availability** | Name exists; no slots in DB | `200 OK` | Empty array: `[]` |
| **Provider Not Found** | Name does not exist in DB | `404 Not Found` | Error object: `{"error": "Provider not found"}` |
| **Validation Error** | Special characters in name | `400 Bad Request` | Error object: `{"error": "Invalid name format"}` |

---

## Technical Constraints for Test Implementation
* **Database Fixtures:** Use a `pytest` fixture to provide a clean database session for each test.
* **Isolation:** Tests must not rely on the state left by previous tests.
* **Assertions:** * Verify the `Content-Type` is `application/json`.
    * Validate the schema of the JSON response, not just the values.