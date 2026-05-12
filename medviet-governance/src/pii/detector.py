# src/pii/detector.py
import importlib.util
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider

def build_vietnamese_analyzer() -> AnalyzerEngine:
    """
    TODO: Xây dựng AnalyzerEngine với các recognizer tùy chỉnh cho VN.
    """

    # --- TASK 2.2.1 ---
    # Tạo CCCD recognizer: số CCCD VN có đúng 12 chữ số
    cccd_pattern = Pattern(
        name="cccd_pattern",
        regex=r"\b\d{11,12}\b",
        score=0.9
    )
    cccd_recognizer = PatternRecognizer(
        supported_entity="VN_CCCD",
        patterns=[cccd_pattern],
        context=["cccd", "căn cước", "chứng minh", "cmnd"],
        supported_language="vi"
    )

    # --- TASK 2.2.2 ---
    # Tạo phone recognizer: số điện thoại VN (0[3|5|7|8|9]xxxxxxxx)
    phone_recognizer = PatternRecognizer(
        supported_entity="VN_PHONE",
        patterns=[Pattern(
            name="vn_phone",
            regex=r"\b0?[35789]\d{8}\b",
            score=0.85
        )],
        context=["điện thoại", "sdt", "phone", "liên hệ"],
        supported_language="vi"
    )

    email_pattern = Pattern(
        name="vn_email",
        regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        score=0.85
    )
    email_recognizer = PatternRecognizer(
        supported_entity="EMAIL_ADDRESS",
        patterns=[email_pattern],
        context=["email", "e-mail", "mail"],
        supported_language="vi"
    )

    # --- TASK 2.2.3 ---
    # Tạo NLP engine dùng spaCy Vietnamese model
    model_name = "vi_core_news_lg" if importlib.util.find_spec("vi_core_news_lg") else "xx_ent_wiki_sm"
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "vi", 
                    "model_name": model_name}]
    })
    nlp_engine = provider.create_engine()

    # --- TASK 2.2.4 ---
    # Khởi tạo AnalyzerEngine và add các recognizer
    name_pattern = Pattern(
        name="vn_person_name",
        regex=r"\b[A-Za-zÀ-Ỵà-ỵ]+(?:\s+[A-Za-zÀ-Ỵà-ỵ]+){1,4}\b",
        score=0.75
    )
    name_recognizer = PatternRecognizer(
        supported_entity="PERSON",
        patterns=[name_pattern],
        context=["tên", "bệnh nhân", "bác sĩ"],
        supported_language="vi"
    )

    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["vi"])
    analyzer.registry.add_recognizer(cccd_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)
    analyzer.registry.add_recognizer(email_recognizer)
    analyzer.registry.add_recognizer(name_recognizer)

    return analyzer


def detect_pii(text: str, analyzer: AnalyzerEngine) -> list:
    """
    TODO: Detect PII trong text tiếng Việt.
    Trả về list các RecognizerResult.
    Entities cần detect: PERSON, EMAIL_ADDRESS, VN_CCCD, VN_PHONE
    """
    results = analyzer.analyze(
        text=text,
        language="vi",
        entities=["PERSON", "EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE"]
    )
    return results
