import io
from reportlab.lib.colors import HexColor

from reportlab.lib import styles
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import HRFlowable

def generate_pdf(history):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    styles["Title"].textColor = HexColor("#0F4C81")
    styles["Heading2"].textColor = HexColor("#1E88E5")
    styles["BodyText"].leading = 20

    styles["Title"].alignment = TA_CENTER
    styles["Heading2"].alignment = TA_CENTER
    styles["BodyText"].spaceAfter = 10

    story = []
    
    logo = Image("assets/Logo1.png", width=90, height=90)
    logo.hAlign = "CENTER"
    story.append(logo)

    story.append(Spacer(1,15))
    story.append(
        Paragraph(
            "<b><font size=22>AI Decision Council Report</font></b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "<font size=16 color='gray'>Multi-Agent Decision Intelligence Report</font>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1,25))

    story.append(
        Paragraph(
            "<b>Prepared By:</b> AI Decision Council",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<b>Version:</b> 1.0",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,20))

    story.append(HRFlowable(width="100%"))
    story.append(Spacer(1,15))


    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<font color='blue'>____________________________________________________________</font>",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,10))


    story.append(
        Paragraph("<br/><br/>", styles["Normal"])
    )

    for row in history:

        story.append(
            Paragraph(
                f"<b>Question:</b> {row[1]}",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                "<font size=18 color='#0B3D91'><b>Executive Summary</b></font>",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                f"<b>Experts:</b> {row[3]}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                f"<b>Risk:</b> {row[2]}%",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,20))
        
        story.append(
            Paragraph(
                f"<b>Confidence:</b> {row[4]}%",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                f"<b>Agreement:</b> {row[5]}%",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,20))

        decision = row[6]

        # Remove Markdown symbols
        decision = decision.replace("####", "")
        decision = decision.replace("###", "")
        decision = decision.replace("##", "")
        decision = decision.replace("**", "")
        decision = decision.replace("■", "")

        # Convert new lines for PDF
        decision = decision.replace("\n", "<br/>")

        story.append(
            Paragraph(
                f"<b>Decision:</b><br/>{decision}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Date:</b> {row[7]}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph("<br/><br/>", styles["Normal"])
        )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf