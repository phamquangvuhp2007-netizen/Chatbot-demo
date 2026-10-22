import streamlit as st
import re

# -----------------------------------------------------------------------------
# 1. CẤU HÌNH TRANG WEB & GIAO DIỆN SHOPEE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Shopee AI Assistant",
    page_icon="🧡",
    layout="centered"
)

st.title("🧡 Trợ lý Mua sắm Shopee AI")
st.caption("Hỗ trợ tra cứu sản phẩm, tóm tắt review, xử lý khiếu nại & tư vấn thông minh")

# -----------------------------------------------------------------------------
# 2. DỮ LIỆU GIẢ LẬP & LỊCH SỬ CHAT (SESSION STATE)
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Chào bạn! Em là Trợ lý AI của Shopee. Bạn cần em hỗ trợ tìm sản phẩm, xem review hay kiểm tra đơn hàng nào ạ? 🧡"}
    ]

# -----------------------------------------------------------------------------
# 3. ENGINE XỬ LÝ NỘI DUNG (LOGIC XỬ LÝ HỘI THOẠI)
# -----------------------------------------------------------------------------
def respond_to_user(user_input: str) -> str:
    text_lower = user_input.lower()
    
    # A. Guardrail - Từ chối Y tế / Pháp lý / Nhạy cảm
    medical_keywords = ["đau bụng", "uống thuốc", "kê đơn", "chữa bệnh", "bệnh lý"]
    if any(kw in text_lower for kw in medical_keywords):
        return ("Shopee không thể đưa ra lời khuyên hoặc tư vấn y tế. Nếu bạn có triệu chứng "
                "bất thường, vui lòng đến cơ sở y tế gần nhất để được bác sĩ thăm khám nhé! 🩺")

    # B. Sentiment & Anti-Churn - Nhận diện phàn nàn & Tung Voucher
    negative_keywords = ["chậm", "tệ", "hoàn tiền", "lừa đảo", "chán", "lâu", "hủy đơn"]
    if any(kw in text_lower for kw in negative_keywords):
        return ("Shopee chân thành xin lỗi bạn về sự bất tiện này ạ! 🥺\n\n"
                "Em đã ghi nhận phản hồi và ưu tiên kiểm tra khẩn cấp đơn hàng cho bạn. "
                "Shopee xin gửi tặng bạn **Mã giảm giá 20K (Mã: SPFIX20K)** đền bù trải nghiệm. "
                "Bạn cho em xin Mã đơn hàng để xử lý ngay nhé!")

    # C. Review Summarization - Tóm tắt Đánh giá
    if "review" in text_lower or "đánh giá" in text_lower:
        if "baseus" in text_lower or "tai nghe" in text_lower:
            return ("📊 **Tóm tắt Review AI cho Tai nghe Bluetooth Baseus Bowie WM02** (4.8/5 ⭐ từ 1.240 đánh giá):\n\n"
                    "👍 **Ưu điểm nổi bật:**\n"
                    "  + Pin trâu (4-5h nghe liên tục)\n"
                    "  + Thiết kế nhỏ gọn, nhiều màu sắc\n"
                    "  + Kết nối bluetooth nhanh, ổn định\n\n"
                    "👎 **Điểm cần lưu ý:**\n"
                    "  - Dải bass hơi mỏng\n"
                    "  - Nút cảm ứng khá nhạy dễ bấm nhầm\n\n"
                    "💰 **Giá hiện tại:** 289.000đ")

    # D. Product Specs - Tra cứu thông số
    if "anessa" in text_lower or "kem chống nắng" in text_lower:
        return ("📌 **Kem chống nắng Anessa Perfect UV Sunscreen Milk**\n\n"
                "• **Dành cho loại da:** Da dầu & Hỗn hợp thiên dầu\n"
                "• **Khả năng kiềm dầu:** Kiềm dầu khô thoáng từ 6 - 8 tiếng\n"
                "• **Giá ưu đãi hôm nay:** 515.000đ (Đã áp mã Freeship Xtra)")

    # E. Out-Of-Scope - Xử lý Ngoài phạm vi (Thời tiết / Giải toán)
    if "thời tiết" in text_lower:
        return ("Dự báo thời tiết hôm nay có thể có mưa đó ạ! ☔\n\n"
                "Nếu bạn chuẩn bị ra ngoài, Shopee gợi ý nhanh vài mẫu **Áo mưa bộ chống thấm** "
                "và **Ô gấp gọn** đang có mã Freeship Xtra nhé!")
                
    if "giải toán" in text_lower or "phương trình" in text_lower:
        return ("Em là Trợ lý Mua sắm Shopee nên chưa được huấn luyện để giải toán rồi ạ! 😅\n\n"
                "Em có thể giúp bạn: Tìm deal hời, kiểm tra đơn hàng, hoặc săn voucher Freeship nè!")

    # F. Grounding Fallback - Không ảo tưởng
    return ("Em đã kiểm tra nhưng chưa tìm thấy thông tin chi tiết này trong hệ thống của Shop.\n\n"
            "Em đã gửi tin nhắn trực tiếp đến Chủ Shop để xác nhận giúp bạn rồi ạ! Bạn chờ phản hồi trong giây lát nhé 🧡")

# -----------------------------------------------------------------------------
# 4. HIỂN THỊ HỘI THOẠI TRÊN STREAMLIT
# -----------------------------------------------------------------------------
# Hiển thị toàn bộ tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận tin nhắn mới từ người dùng
if prompt := st.chat_input("Nhập câu hỏi của bạn tại đây..."):
    # Hiển thị câu hỏi của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tạo phản hồi từ Chatbot
    bot_response = respond_to_user(prompt)
    
    # Hiển thị câu trả lời của Chatbot
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
