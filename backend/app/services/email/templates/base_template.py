def base_email_template(content: str, cta_url: str = "", cta_text: str = ""):

    button_html = ""

    if cta_url and cta_text:
        button_html = f"""
        <div style="text-align:center; margin:30px 0;">
          <a href="{cta_url}"
            style="background:#4f46e5; color:white; padding:12px 24px;
            text-decoration:none; border-radius:8px; font-weight:bold; display:inline-block;">
            {cta_text}
          </a>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;background:#f4f6f8;font-family:Arial">

      <table width="100%" style="padding:40px 0;">
        <tr>
          <td align="center">

            <table width="600" style="background:white;border-radius:12px;overflow:hidden;">

              <tr>
                <td style="background:#111827;padding:24px;text-align:center;">
                  <h2 style="color:white;margin:0;"><span style="color:#0d6efd">Talent</span> Finder</h2>
                </td>
              </tr>

              <tr>
                <td style="padding:30px;color:#111827;">
                  {content}
                  {button_html}
                </td>
              </tr>

              <tr>
                <td style="padding:20px;text-align:center;font-size:12px;color:#9ca3af;">
                  Talent Finder
                </td>
              </tr>

            </table>

          </td>
        </tr>
      </table>

    </body>
    </html>
    """
