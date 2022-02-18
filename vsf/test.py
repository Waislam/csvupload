import requests

html = "https://imgs.hcaptcha.com/22b5qlQ9ggIwoGkLYFHnpUATmzg7XSUDqH890WJ2reGRTNVqCARHEMaCPpSqySUpUd2h4TQzzhUYbJCRTcaM+xDaXoP2ijn2w+ENDeiCvDP6ucNWmHsbXbDqIXAeMFN6W+ttg4OcOBWjz1vlY59bhSAzPwvBCGMcxXOpWagqZWgm1Y5jG4p99JaSuaHQhJRp90hnTgQc2euza9MCOQgYutgD&quot"
html1 = "https://imgs.hcaptcha.com/e8Ej56GfR4HvTCPLhbxOi6YBeQ1KPOxaeQ8e8FClXU196Ber8cA5ui3PXdSD4oZatuAWSsjyoSNNpMVxjklvV706LMo6GyzAlTZk2jco3fhkntuyHHd1+xkT8aPXpgWCU6iizNPH+YOzn1FRn+eK3c4ihxlqdRuypHr1r6yLfyIJJ7jC52miSUUtVyyoglrT9ImHm8ye4v3RE69KxU4=Td1PZBM2McbHUYDT"
html2 = "https://imgs.hcaptcha.com/IJSFsChXAspw3UbvGRr3sN6tzUixrtzMSH81xlu+NcvPU/7pHl9NV1m6yCU1X53GjYvZVgPM9UYQSmmLiKx4M8nNdkmEEdKIubX1jhEwbh40E+FVs3ACaEWplQSiLVHTl/EFlh/cmm71KFo4cIVZWL35oNh6KWlJtEcVCgmavgEm1EMXA39FBR9DMIg6tn/da65S0g==pS0IVZR6+cRA0Qsk"
head = 'boat'
l = [html, html1, html2]
for item in l:
    if head == 'bus':
        if '==' in item:
            print(item)
    else:
        if '=' not in item:
            print(item)