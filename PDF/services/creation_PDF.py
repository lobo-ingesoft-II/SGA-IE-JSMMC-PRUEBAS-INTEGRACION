from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os  
from PDF.services.pdf_bd_peticiones import create_log_pdf, get_next_id
from PDF.backend.database import get_db

## Input Data PDF 
def input_data():
    """This function is a example of how to input data for the PDF generation."""
    data = [["Kind of Test", "Probe name", ["Result", "description", "date", "etc"]],
           ["FrontEnd", "Test 1", ["Passed", "Everything is ok", "2023-10-01", "etc"]],
            ["FrontEnd", "Test 1", ["Passed", "Everything is ok", "2023-10-01", "etc"]],
             ["FrontEnd", "Test 1", ["Passed", "Everything is ok", "2023-10-01", "etc"]],
              ["FrontEnd", "Test 1", ["Passed", "Everything is ok", "2023-10-01", "etc"]],
               ["FrontEnd", "Test 1", ["Passed", "Everything is ok", "2023-10-01", "etc"]],
                ["FrontEnd", "Test 1", ["Passed", "Everything is ok", "2023-10-01", "etc"]],
                 ["FrontEnd", "Test 1", ["Passed", "Everything is ok", "2023-10-01", "etc"]],
                  ["FrontEnd", "Test 1", ["Passed", "Everything is ok", "2023-10-01", "etc"]],
           ["BackEnd", "Test 2",  ["Passed", "Everything is ok", "2023-10-01", "etc"]]
           ]
    
    return data


def check_if_page_full(c, y):
    """Check if the page is full and create a new page if it is."""
    if y < 50:  # If the y coordinate is less than 50, create a new page
        c.showPage()
        c.setFont("Helvetica", 12)
        return 750  # Reset y to the top of the new page
    return y

def createPDF(TestName:str, data):
    
    # get the next id for the log
    db = next(get_db())
    id = get_next_id(db)

    # define the file name and path 
    fileName = TestName + "_" + str(id) + ".pdf"
    OutPath = os.path.join("PDF_TEST", fileName)

        # create the directory if it does not exist 
    os.makedirs(os.path.dirname(OutPath), exist_ok=True)

    print(f"Generando PDF en: {OutPath}")

    #-----------------------------Creation PDF -------------------------------
    # create a canvas object 
    c = canvas.Canvas(OutPath, pagesize=LETTER)
    c.setFont("Helvetica", 12)

    # Ruta a tu imagen

    # Base directory = carpeta donde está este archivo .py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Ruta segura a la imagen
    img_path = os.path.join(BASE_DIR, "..", "images", "escudoUnal.png")  # Si estás dentro de PDF/

    # Normaliza la ruta
    img_path = os.path.normpath(img_path)
    # Imagen Escudo 
    c.drawImage(img_path, x=450, y=680, width=150, height=150, preserveAspectRatio=True, mask='auto')


    # Draw the title of the PDF
    x = 50
    y = 730  # first coordinate for the y-axis 

    c.drawString(x+200,y , TestName + "_" + str(id))
    y -= 30
    c.drawString(180, y, "Resultados de las pruebas de integración")
    
    

    y -= 30

    for test in data:
        print(test)

        kindTest = test[0]  # Kind of test
        nameTest = test[1]
        Result = test[2]
        # Draw the label for the kind of test
        label = f"Tipo de prueba: {kindTest}"
        c.drawString(x, y, label)
        y -= 15

            # Si se acaba la página
        y = check_if_page_full(c, y)

        # Draw the name of the test
        label = f"Nombre de la prueba: {nameTest}"
        c.drawString(x, y, label)
        y -= 15

            # Si se acaba la página
        y = check_if_page_full(c, y)

        # Draw the result 
        label = f" Resultados: "
        c.drawString(x, y, label)
        y -= 15

            # Si se acaba la página
        y = check_if_page_full(c, y)

        # Draw the result of the test
        for result in Result:
            # Draw the result
            label = f"      * {str(result)}"
            c.drawString(x, y, label)
            y -= 15
          
            # Si se acaba la página
            y = check_if_page_full(c, y)



    c.save()
    #-----------------------------End Creation PDF -------------------------------
    # Save the log in the database
    create_log_pdf(db, name=fileName)
    print(f"PDF generado: {fileName}")

