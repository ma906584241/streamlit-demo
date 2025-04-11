import streamlit as st
from Dify.Comlan_Demo.db_manager import DatabaseManager
import hashlib

class LoginManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        self.db_manager.init_db()
        hashed_password = self.hash_password(password)
        return self.db_manager.register_user(username, hashed_password)

    def verify_user(self, username, password):
        self.db_manager.init_db()
        hashed_password = self.hash_password(password)
        return self.db_manager.verify_user(username, hashed_password)

    def render_login_page(self):
        st.set_page_config(page_title="ComLan 智能助手", layout="wide")  # 设置页面配置
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            # Inject custom CSS styles
            st.markdown("""
            <style>
                /* Main container style */
                .main {
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    height: 100vh;
                }
                /* Button styles */
                .stButton>button {
                    border-radius: 25px;
                    background: #0072C6;  /* Brand color */
                    color: white;
                    width: 100%;
                    padding: 0.8rem;
                    font-weight: bold;
                    transition: all 0.3s;
                }
                                .stButton>button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 114, 198, 0.4);
                }
                
                /* Tab styles */
                [data-baseweb="tab-list"] {
                    gap: 10px;
                }
                
                [data-baseweb="tab"] {
                    padding: 12px 30px;
                    border-radius: 30px;
                    background: #f0f0f0;
                    transition: all 0.3s;
                    color: #666;  /* 建议改为更柔和的颜色 */
                }
                
                [data-baseweb="tab"]:hover {
                    background: #e0e0e0;
                }
                
                [data-baseweb="tab"][aria-selected="true"] {
                    background: #0072C6;
                    color: white;
                }
            </style>
            """, unsafe_allow_html=True)

            # Create a responsive layout
            col1, col2, col3 = st.columns([1, 4, 1])
            
            with col2:
                # Add card container
                with st.container():
                    st.markdown("<div class='form-card'>", unsafe_allow_html=True)
                    
                    # Add title and icon
                    st.markdown("""
                        <div style='text-align: center; margin-bottom: 2rem;'>
                            <h1 style='color: #0072C6; margin-bottom: 0.5rem;'>⚙️ ComLan 智能助手</h1>
                            <p style='color: #666;'>您的智能对话分析专家</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    tab1, tab2 = st.tabs(["🔑 用户登录", "📝 新用户注册"])
                    
                    with tab1:
                        login_username = st.text_input("用户名", key="login_username")
                        login_password = st.text_input("密码", type="password", key="login_password")
                        
                        if st.button("🚀 立即登录"):
                            if self.verify_user(login_username, login_password):
                                st.session_state.logged_in = True
                                st.success("✅ 登录成功！")
                                st.rerun()
                            else:
                                st.error("❌ 用户名或密码错误！")
                    
                    with tab2:
                        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)  # 添加背景样式
                        reg_username = st.text_input("用户名", key="reg_username")
                        reg_password = st.text_input("密码", type="password", key="reg_password")
                        reg_password2 = st.text_input("确认密码", type="password", key="reg_password2")
                        
                        if st.button("✨ 立即注册"):
                            if reg_password != reg_password2:
                                st.error("🔒 两次输入的密码不一致！")
                            elif self.register_user(reg_username, reg_password):
                                st.success("🎉 注册成功！请返回登录页面进行登录。")
                        st.markdown("</div>", unsafe_allow_html=True)  # 结束背景样式

                    st.markdown("</div>", unsafe_allow_html=True)  # End card container

        return st.session_state.logged_in
