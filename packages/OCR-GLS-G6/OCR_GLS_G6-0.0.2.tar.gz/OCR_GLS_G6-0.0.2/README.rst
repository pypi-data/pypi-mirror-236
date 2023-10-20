(OCR-GLS-G6) OCR
================

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install OCR-GLS-G6

วิธีใช้
~~~~~~~

.. code:: python

   from OcrTools import *

   img_path="simple.pdf" // ไฟล์ PDF หรือ ไฟล์รูปภาพ

   OcrTools.easyOCR(typeOfOcr="qrcode",locationFile=img_path,area={'offset_x_min':2078,'offset_y_min':3152,'width':213,'height':220})

   // Output
   {   
       'coordinates': [ตำแหน่งของไฟล์ที่อ่านข้อมูล],
       'value': ข้อความที่ได้จาก QR หรือ ข้อความในไฟล์ที่ต้องการ,
       'valid': ความถูกต้องของข้อมูล
       'accuracy_percent': เปอร์เซ็นความถูกต้องของข้อมูล
   }

พัฒนาโดย: Burin Panchat GLS Develop G6
