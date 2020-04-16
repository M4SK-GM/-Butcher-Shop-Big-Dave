minutes = [75, 175, 125, 200, 50, 300, 150, 250, 250, 125, 150, 50]
gigi = [1.25, 1.25, 0.75, 1.5, 2.5, 3.5, 3, 1, 2, 0.75, 0.5, 1.75]
print(f'2018:')
for i in range(1, 13):
    if minutes[i - 1] > 250:
        minplus = (minutes[i - 1] - 250) * 4
    else:
        minplus = 0
    if gigi[i - 1] > 2:
        gig = gigi[i - 1] - 2
        gigpl = 0
        while gig > 0:
            gig -= 0.5
            gigpl += 1
        gigplus = gigpl * 140
    else:
        gigplus = 0
    print(f'{i}: {300 + minplus + gigplus}')
