CSS = """
<style>
  #MainMenu { visibility: hidden; }
  footer    { visibility: hidden; }
  header    { visibility: hidden; }

  .block-container { padding-top: 1.5rem !important; max-width: 760px; }

  /* Tarjeta de comportamiento */
  .comp-card {
    background: #fff;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    border-left: 5px solid #ccc;
  }
  .comp-nombre { font-weight: 700; font-size: 15px; color: #1a1a2e; margin-bottom: 4px; }
  .comp-desc   { font-size: 13px; color: #666; line-height: 1.5; }

  /* Header de dimensión */
  .dim-header {
    padding: 12px 16px;
    border-radius: 8px;
    margin: 22px 0 10px;
    color: #fff;
    font-weight: 700;
    font-size: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* Progress bar */
  .prog-wrap  { background: #e9ecef; border-radius: 10px; height: 8px; margin: 8px 0 18px; }
  .prog-bar   { height: 8px; border-radius: 10px;
                background: linear-gradient(90deg,#1a3a5c,#2980b9);
                transition: width 0.3s ease; }

  /* Botón primario */
  .stButton > button {
    background: linear-gradient(135deg, #1a3a5c, #2980b9) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2rem !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    width: 100%;
  }
  .stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(26,58,92,0.3) !important;
  }

  /* Sliders */
  .stSlider > label { font-weight: 600 !important; font-size: 14px !important; }
</style>
"""
