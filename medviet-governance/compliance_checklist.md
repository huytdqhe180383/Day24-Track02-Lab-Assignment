# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [X] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [X] Backup cũng phải ở trong lãnh thổ VN
- [X] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [X] Thu thập consent trước khi dùng data cho AI training
- [X] Có mechanism để user rút consent (Right to Erasure)
- [X] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [X] Có incident response plan
- [X] Alert tự động khi phát hiện breach
- [X] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [X] Đã bổ nhiệm Data Protection Officer
- [X] DPO có thể liên hệ tại: ___

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | 🚧 In Progress | Infra Team |
| Audit logging | CloudTrail + API access logs | ⬜ Todo | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus) | ⬜ Todo | Security Team |

## F. Kế hoạch cho các mục còn thiếu
Với mỗi row còn "⬜ Todo", mô tả technical solution cụ thể sẽ implement:

- **Audit logging (⬜ Todo)**: 
	- Bật FastAPI middleware log request/response metadata (không log PII) và đẩy vào OpenSearch.
	- Lưu audit trail cho mọi hành động đọc/ghi/xóa với các trường: `user_id`, `role`, `resource`, `action`, `timestamp`, `request_id`.
	- Thiết lập retention policy 180 ngày và cảnh báo khi có access bất thường.

- **Breach detection (⬜ Todo)**:
	- Prometheus scrape API metrics + audit logs; tạo alert rules (spike read/delete, 5xx, auth failures).
	- Grafana dashboard cho alert triage; tích hợp Slack/Email với mức độ severity.
	- Playbook tự động: khi alert nghiêm trọng → tạo incident ticket + freeze token của user nghi vấn.
