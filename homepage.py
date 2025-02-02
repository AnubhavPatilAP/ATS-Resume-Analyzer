import streamlit as st

# Page Configuration
st.set_page_config(page_title="Resume Analyser", page_icon="📄", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(180deg, #4B0082, #800080);
            font-family: 'Arial', sans-serif;
            color: white;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 20px 0;
        }
        .hero-section {
            text-align: center;
            padding: 40px;
            background-color: rgba(75, 0, 130, 0.8);
            border-radius: 15px;
            margin-bottom: 40px;
        }
        .hero-section h1 {
            font-size: 36px;
        }
        .hero-section p {
            font-size: 18px;
        }
        .hero-section button {
            background-color: #6a0dad;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        .hero-section button:hover {
            background-color: #5e008a;
        }
        .column-container {
            display: flex;
            justify-content: space-between;
            gap: 20px;
        }
        .column {
            background-color: rgba(128, 0, 128, 0.9);
            border-radius: 10px;
            padding: 20px;
            width: 48%;
            text-align: center;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            padding: 20px 0;
            border-top: 1px solid white;
        }
        .footer .footer-links {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .footer .footer-links div {
            text-align: left;
        }
        .footer .footer-links h4 {
            margin-bottom: 10px;
        }
        .footer .social-links {
            margin-top: 10px;
        }
        .footer .social-links a {
            margin-right: 15px;
            color: white;
            text-decoration: none;
        }
        .form-group input, .form-group button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
        }
        .form-group button {
            background-color: #6a0dad;
            color: white;
            font-size: 16px;
            cursor: pointer.
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation logic
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    # Header Section
    st.markdown("<div class='header'><h1>Resume Analyser</h1></div>", unsafe_allow_html=True)

    # Hero Section
    st.markdown(
        """
        <div class='hero-section'>
            <h1>Unlock your potential with AI-powered resume analysis.</h1>
            <p>Tailored for individuals and enterprises to enhance impact and drive career success.</p>
            <button>Get Started</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Two Columns Section
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("<div class='column-container'>", unsafe_allow_html=True)

    # Individual Section
    with st.container():
        st.markdown(
            """
            <div class='column'>
                <h3>For Individual</h3>
                <p>Get personalized insights and expert tips to elevate your resume and land your dream job faster.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Button to navigate
        if st.button("Analyze as Individual"):
            st.session_state.page = "IndividualAnalyzer"

    # Enterprise Section
    st.markdown(
        """
        <div class='column'>
            <h3>For Enterprise</h3>
            <p>Streamline hiring with data-driven resume analysis, empowering your team to identify top talent quickly and efficiently.</p>
            <div class="form-group">
                <input type="email" placeholder="Email">
                <input type="password" placeholder="Password">
                <button>Login</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer Section
    st.markdown(
        """
        <div class='footer'>
            <div class='footer-links'>
                <div>
                    <h4>HELP</h4>
                    <p>Analysis Metrics?</p>
                    <p>How to Use?</p>
                    <p>Sustainability</p>
                </div>
                <div>
                    <h4>ABOUT</h4>
                    <p>Our story</p>
                    <p>How to Use?</p>
                </div>
                <div>
                    <h4>LEGAL STUFF</h4>
                    <p>Terms of use</p>
                    <p>Terms of sale</p>
                    <p>Privacy policy</p>
                </div>
            </div>
            <div class='social-links'>
                <a href="#">Facebook</a>
                <a href="#">Twitter</a>
                <a href="#">LinkedIn</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif st.session_state.page == "IndividualAnalyzer":
    # Redirect to the specific page
    st.query_params["page"] = "pages/IndividualAnalyzer"
    st.write("Redirecting to Individual Analyzer...")
