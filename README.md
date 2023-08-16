# summer-reu
This program takes 3 user inputs: the desrired number of UEs observed, 
the coordinates of the land we're examining, and the radius of the 
wireless cells' reach. The output of the program is a suggested list of where to place cells to ensure coverage for each UE while also creating shared paths 
of wireless cells to minimize supposed future costs.

The program runs as such:

    1. generateRandomUEs(): is randomly generates input number of UEs
    within the given land

    2. findShared(): determines if any pair of UEs could share one 
    wireless cell right off the bat (i.e. they are within 2 wireless 
    radii from each other). Puts down all the initial wireless cells 
    around the UEs that can share and those not able to share

    3. Next, we find the closest distance to road and what the coordinates
    of that point on the closest road for each wireless cell. We also 
    "mark" all cells in preparation for the next step.

    4. createSharedPaths(): determines if reasonably distanced pairs of
    cells could share a path -- if so, places a new wireless cell in 
    between the existing cells. Then, it looks at which cell in the 
    sharing path is closest to a road; it "unmarks/removes" the cells 
    that are further than it (so only the closest one stays "marked")

    4. makeWirelessPath(): takes all "marked" cells from the previous 
    steps, and creates a perpendicular path of wireless cells to the 
    nearest road

Note: the list named "finalLeaves" is actually a misnomer now that I
think of it, because the cells in there are not actually the final leaves.
They are just the last child cell of the perpendicular path of cells 
that are eventually going to be laid down (not the actual last leaf in the
overall path though).

