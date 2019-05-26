from pdfs import *

e = PDFEngine(text="""[00:03:00] Speaker 2: This is Abby.
[00:09:00] Speaker 3: Hey Abby, this is Anis.
[00:09:00] Speaker 1: Hello. Is anyone there?
[00:14:00] Speaker 2:  Yeah, we're here Kerry. How are you doing?
[00:17:00] Speaker 1:  Oh great to hear you guys. How are you?
[00:20:00] Speaker 2:  I'm doing well. You're nice.
[00:21:00] Speaker 3:  All right, that's cut the chitchat get the business.
[00:23:00] Speaker 1:  How many money did you guys make last week?
[00:28:00] Speaker 2:  Okay, that's enough.
[00:28:00] Speaker 3:  It's not about the money. It's about the number Tau that we have.
[00:32:00] Speaker 1:  Oh, yes. I saw 70% growth from last one great work.
[00:31:00] Speaker 2:  All right, the car has to be less than a minute. So let them eat here.
[00:39:00] Speaker 3:  your oldest""", participants=["+12102683553", "+16502857265", "+12102683553"])
print(e.pdf_url)
e.textPDF()
