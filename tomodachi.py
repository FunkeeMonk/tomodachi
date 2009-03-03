#!/usr/bin/python
import sys, tarfile, urllib, string, os, time

# From username, grab all game records and unarchive them                                                   
# http://www.gokgs.com/gameArchives.jsp?user=Heretix&oldAccounts=y
# http://www.gokgs.com/servlet/archives/en_US/Heretix-all-2008-12.tar.gz

delay = 5

def get_month_year(anchor):                                            
	href = anchor['href']
	yearstart = href.find('year=')+5
	monthstart = href.find('month=')+6
	return int(href[monthstart:]), int(href[yearstart:yearstart+4])

def main(argv):                                 
	
	# usage:
	# <username> <start MMYYYY (optional)> <end MMYYYY(optional)>

	if len(argv) < 1 or len(argv) == 2 or len(argv) > 3:
		print "Downloads KGS SGF game records."
		print "Usage: GrabKGSArchive <KGS username> (<start (MMYYYY)> <end (MMYYYY)> (optional))"
		print "Example: GrabKGSArchive Heretix (grab all game records for Heretix (except for current month))"
		print "Example: GrabKGSArchive Heretix 042003 022009 (grab all game records from April 2003 to Feb 2009)"
		sys.exit()
		
 	username = argv[0]

	if len(argv) == 1:
		# Find start/time end period
		from BeautifulSoup import BeautifulSoup
		import web
		                                                                   
		webURL = "http://www.gokgs.com/gameArchives.jsp?user=" + username + "&oldAccounts=y"
		s = web.get(webURL)
		soup = BeautifulSoup(s)
	
		tableContainers = soup.findAll("table", "grid")

		if len(tableContainers) == 2:
	   		rows = tableContainers[1].findAll('a')
		else:
			rows = tableContainers[0].findAll('a')

		(currentMonth, currentYear) = get_month_year(rows[0])
		(endMonth, endYear) = get_month_year(rows[len(rows) - 1])
	else:
		currentMonth = int(argv[1][:2])
		currentYear = int(argv[1][2:6])
		endMonth = int(argv[2][:2])
		endYear = int(argv[2][2:6])

	urlhead = "http://www.gokgs.com/servlet/archives/en_US/" + username + "-all-"
	print "Downloading game records from " + str(currentMonth) + "/" + str(currentYear) + " to " + str(endMonth) + "/" + str(endYear)
	while currentYear <= endYear:
		while currentMonth <=12:
			url = urlhead + str(currentYear) + "-" + str(currentMonth) + ".tar.gz"
			filename = str(currentYear) + "-" + str(currentMonth) + ".tar.gz"
			print "Downloading records from " + str(currentMonth) + "/" + str(currentYear)
			urllib.urlretrieve(url, filename)                                                            
			
			if tarfile.is_tarfile(filename):
				tar = tarfile.open(filename)
			 	tar.extractall(username)
			 	tar.close()
			os.remove(filename)
			
			currentMonth = currentMonth + 1
			
			if (currentYear == endYear and currentMonth > endMonth):
				break
			
			time.sleep(delay)
		currentYear = currentYear + 1
		currentMonth = 1

if __name__ == "__main__":
    main(sys.argv[1:])