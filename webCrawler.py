#CSE 5311 - WEB CRAWLER
#REFER TO readme file before compiling and running this code
#Manoj Kumar
#Prasanna
#Syed Hannan Yunus

import urllib
#-------------------------------------------------------------------------------

#GETS THE PAGE SOURCE CODE!
def get_page(url):
    try:
        source_code = urllib.urlopen(url)
        page = source_code.read()
        source_code.close()
        return page
    except:
        return ""
    return ""

# GETS ALL THE HREF FROM SOURCE CODE!
def get_links(start_link):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(get_page(start_link))

    link_lst = []
    for link in soup.find_all('a'):
        link = (link.get('href'))
        link_lst.append(link)
    return link_lst

#GETS ONLY THE CSE.UTA.EDU LINKS ON THE PAGE
def extract_cse_links(start_link):
    new_link_lst = []
    url_lst = get_links(start_link)
    for link in url_lst:
        if link == None or link == "":
            pass
        elif link.startswith("/"):
            link = "http://cse.uta.edu" + link
            new_link_lst.append(link)
        elif ".html" in link and "http" not in link:
            link = start_link + link
            new_link_lst.append(link)

    #Remove unwanted links,pages,etc
    pure_list = []
    for item in new_link_lst:
        if "GAANN" in item:
            pass
        elif item[len(item)-1:]== "/":
            pure_list.append(item[:len(item)-1])
        elif ".pdf" in item or ".doc" in item:
            pass
        else:
            pure_list.append(item)
    return pure_list
#--------------------------------------------------------------------------------

#Crawl Function crawls the cse.uta.edu domain
def crawl(seed):
    tobe_crawled = [seed]
    visited_link = []
    link_dictionary = {}
    while tobe_crawled:
        page = tobe_crawled.pop(0)
        if page not in visited_link:
            link_in_page = extract_cse_links(page)
            link_dictionary[page] = link_in_page
            visited_link.append(page)
            for items in link_in_page:
                if items not in tobe_crawled:
                    tobe_crawled.append(items)
                else:
                    pass
    return link_dictionary

complete_dictionary = crawl("http://cse.uta.edu")

# NetworkX is used to apply Dijkstra's Algo
import networkx as nx
graph = nx.DiGraph(complete_dictionary)

def diameter_dic(graph):
    ds = {}
    for start_nodes in graph:
        distance_dic, path_dic = nx.single_source_dijkstra(graph,start_nodes)
        far_node = max(distance_dic, key=distance_dic.get) #Farthest Node
        ds[start_nodes] = [far_node]
        dis_from_far_node = distance_dic[far_node]
        ds[start_nodes].append(dis_from_far_node)

    return ds

new_dic = diameter_dic(graph)

#Computes the diameter of the graph
def diameter(new_dic):
    max_diameter = 0
    end_node = None
    start_node = None
    for item in new_dic:
        if new_dic[item][1] > max_diameter:
            max_diameter = new_dic[item][1]
            end_node = new_dic[item][0]
            start_node = item

    print "Diameter of the underlying graph:",max_diameter
    print "The two end nodes of the underlying graph:", start_node,"and",end_node
    return start_node, end_node


start_node,end_node = diameter(new_dic)

#Print out the links in the two links for which the diameter is calculated
def link_btw_graph(complete_dictionary):
    for item in new_dic:
        if item == start_node:
            print "URLs in the first node :",complete_dictionary[start_node]
        elif item == end_node:
            print "URLs in the other node:", complete_dictionary[end_node]

link_btw_graph(complete_dictionary)

print ""
print "-"*40, "End of first part of program", "-"*40
print ""

#Prints out the outbound and inbound URLs of the links
outbound_link = []
inbound = []
to_check = None
for items in complete_dictionary:
    outbound_link = (complete_dictionary[items])
    print "Outbound Links of:",items,":",outbound_link
    outbound_link = []
    to_check = items
    for link in complete_dictionary:
        for values in complete_dictionary[link]:
            if to_check == values:
                inbound.append(link)
    print "Inbound links of:",items,":",inbound
    print "#"*10
    to_check = None
    inbound = []

print "-"*40, "End of program", "-"*40
