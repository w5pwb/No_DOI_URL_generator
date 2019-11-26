# No_DOI_URL_generator
Retrofit Company of Biologist URLs in FlyBase


Many links within the FlyBase database did not have a proper link to the paper on the proper Company of Biologists website.  The links used the pubmed ID to generate a link that led to the paper through pubmed.  So for examle, a paper in Development might have the pubmed ID 22791894 but, because FlyBase has no associated DOI for it, a proper link was never established.  Instead the link in FlyBase would have been something like "https://www-ncbi-nlm-nih-gov/pubmed/?term=22791894" which may become obsolete at some point.  A proper link to the paper would be direct to the DEvelopment website i.e. "https://dev-biologists-org.libproxy.unm.edu/content/139/16/3040.long".

I was given the task of using Python to identify all Company of Biologist journal articles within FLyBase that needed new links and generate proper URLs for them.  

The issue was complicated by the inclusion of supplemental materials, papers that have no DOI, and papers that have incomplete volume/issue/page format. 

The project generated URLs for approx 1500 papers that were then corrected in the database.



From an email chain outlining the problem.

"some papers that we will want to link to on the Freq Used Gal4 table do not have any link to the paper other than the Pubmed ID on their FBrf page (example: FBrf0064375) - no DOI, no "Journal website" link.  The pages might well have DOIs, we just don't have them associated. "

"So appending the PMID to that base URL would be one way of making these links in FlyBase, or using the /volume/issue/page format is another (which is what the PMID URL resolves to).
Not sure whether there’s an easy, automatable way for IU to create this type of link for use in FlyBase (on FBrf pages and the GAL4 table)?  E.g. for a given set of journals (maybe just Development and Journal of Cell Science?), create a link using the PMID using the base URL above?

An alternative approach would be to use the URL field of the publication PROFORMA to add these URL links to the chado database - we could do the retrofit relatively easily."
