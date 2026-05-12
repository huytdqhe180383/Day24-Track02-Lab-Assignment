# src/quality/validation.py
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite

def build_patient_expectation_suite() -> ExpectationSuite:
    """
    TODO: Tạo expectation suite cho anonymized patient data.
    """
    context = gx.get_context()
    suite = context.add_or_update_expectation_suite("patient_data_suite")

    # Lấy validator
    df = pd.read_csv("data/raw/patients_raw.csv")
    validator = context.sources.pandas_default.read_dataframe(df)

    # --- TASK: Thêm các expectations ---

    # 1. patient_id không được null
    validator.expect_column_values_to_not_be_null("patient_id")

    # 2. TODO: cccd phải có đúng 12 ký tự
    validator.expect_column_value_lengths_to_equal(
        column="cccd",
        value=12
    )

    # 3. TODO: ket_qua_xet_nghiem phải trong khoảng [0, 50]
    validator.expect_column_values_to_be_between(
        column="ket_qua_xet_nghiem",
        min_value=0,
        max_value=50
    )

    # 4. TODO: benh phải thuộc danh sách hợp lệ
    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    validator.expect_column_values_to_be_in_set(
        column="benh",
        value_set=valid_conditions
    )

    # 5. TODO: email phải match regex pattern
    validator.expect_column_values_to_match_regex(
        column="email",
        regex=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    # 6. TODO: Không được có duplicate patient_id
    validator.expect_column_values_to_be_unique(column="patient_id")

    validator.save_expectation_suite()
    return suite


def validate_anonymized_data(filepath: str) -> dict:
    """
    TODO: Validate anonymized data.
    Trả về dict: {"success": bool, "failed_checks": list, "stats": dict}
    """
    df = pd.read_csv(filepath)
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    # Check 1: Không còn CCCD gốc dạng số thuần túy
    # (sau anonymization, cccd phải là fake hoặc masked)
    raw_df = pd.read_csv("data/raw/patients_raw.csv")
    raw_cccd_set = set(raw_df["cccd"].astype(str))
    if df["cccd"].astype(str).isin(raw_cccd_set).any():
        results["success"] = False
        results["failed_checks"].append("cccd_replaced")

    # Check 2: Không có null values trong các cột quan trọng
    important_cols = ["patient_id", "cccd", "so_dien_thoai", "email", "benh", "ket_qua_xet_nghiem"]
    missing_cols = [col for col in important_cols if col not in df.columns]
    if missing_cols:
        results["success"] = False
        results["failed_checks"].append(f"missing_columns: {missing_cols}")
    else:
        if df[important_cols].isnull().any().any():
            results["success"] = False
            results["failed_checks"].append("null_values")

    # Check 3: Số rows phải bằng original
    if len(df) != len(raw_df):
        results["success"] = False
        results["failed_checks"].append("row_count_mismatch")

    return results
