# generate_report.py

import datetime

def generate_html_report(metrics_list, product_images, output_file="reports/full_report.html"):
    with open("reports/report_template.html", "r") as f:
        template = f.read()

    rows = ""
    for m in metrics_list:
        rows += f"""
        <tr>
          <td>{m['product']}</td>
          <td>{m['roi']:.2f}</td>
          <td>{m['sharpe_ratio']:.2f}</td>
          <td>{m['max_drawdown']:.2%}</td>
          <td>${m['final_equity']:.2f}</td>
        </tr>
        """

    imgs = ""
    for img_path in product_images:
        imgs += f'<img src="../{img_path}" alt="Equity Curve">'

    html = template.replace("{{ generated_time }}", datetime.datetime.utcnow().isoformat())
    html = html.replace("{{ table_rows }}", rows)
    html = html.replace("{{ images }}", imgs)

    with open(output_file, "w") as f:
        f.write(html)

    print(f"✅ HTML report generated: {output_file}")