def test():
    c = Canvas('codecharts.pdf')
    c.setFont('Helvetica-Bold', 24)
    c.drawString(72, 750, 'Testing code page charts')
    cc1 = SingleByteEncodingChart()
    cc1.drawOn(c, 72, 500)

    cc2 = SingleByteEncodingChart(charsPerRow=32)
    cc2.drawOn(c, 72, 300)

    cc3 = SingleByteEncodingChart(charsPerRow=25, hex=0)
    cc3.drawOn(c, 72, 100)

##    c.showPage()
##
##    c.setFont('Helvetica-Bold', 24)
##    c.drawString(72, 750, 'Multi-byte Kuten code chart examples')
##    KutenRowCodeChart(1, 'HeiseiMin-W3','EUC-H').drawOn(c, 72, 600)
##    KutenRowCodeChart(16, 'HeiseiMin-W3','EUC-H').drawOn(c, 72, 450)
##    KutenRowCodeChart(84, 'HeiseiMin-W3','EUC-H').drawOn(c, 72, 300)
##
##    c.showPage()
##    c.setFont('Helvetica-Bold', 24)
##    c.drawString(72, 750, 'Big5 Code Chart Examples')
##    #Big5CodeChart(0xA1, 'MSungStd-Light-Acro','ETenms-B5-H').drawOn(c, 72, 500)

    c.save()
    print('saved codecharts.pdf')
