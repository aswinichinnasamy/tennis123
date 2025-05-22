use ma37;
SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_write_timeout = 600;

-- q1 List all the competitions along with their category name:
select competition_name,category_name
from competitions_table join categories_table
on competitions_table.category_id = categories_table.category_id;

-- q2 Find the number of competitions in each category
select cat.category_name,count(competition_id)
from competitions_table as ct join categories_table as cat
on ct.category_id = cat.category_id
group by category_name;

-- q3 Find all the competitions of type "Doubles"
select competition_name,type 
from competitions_table
where type = "doubles";

-- q4 Get all the competitions that belong to the specific category
select ct.category_id, GROUP_CONCAT(cot.competition_name)
from competitions_table as cot join categories_table as ct
on cot.category_id = ct.category_id
group by ct.category_id;

-- q5 Identify parent competitions and sub-competitions
SELECT parent_id, GROUP_CONCAT(competition_name) as sub_competitions 
FROM competitions_table 
WHERE parent_id IS NOT NULL 
group by parent_id;

-- q6 Analyse the distribution of competition types by category:
select ct.category_id,group_concat(type)
from competitions_table as cot join categories_table as ct
on cot.category_id = ct.category_id
group by category_id;

-- q7 List all the competitions with no parent(top-level competitions)
select competition_name,parent_id
from competitions_table
where parent_id IS NULL;

-- q8 List all the venues along with their associated complex name
select venue_name,complex_name
from complexes_table join venues_table
on complexes_table.complex_id = venues_table.complex_id;

-- q9 Count the number of venues in each complex
select complex_name,count(venue_id) as count
from complexes_table as ct join venues_table as vt
on ct.complex_id = vt.complex_id
group by complex_name;

-- q10 Get the details of venues in a specific country
select country_name,venue_id,venue_name as venues
from venues_table;

-- q11 identify all venues and their timezones
select venue_id,venue_name,timezone
from venues_table;

-- q12 Find the compelexes that have more than one venue
select ct.complex_id, count(venue_id) as count_of_venues
from complexes_table as ct join venues_table as vt
on ct.complex_id = vt.complex_id
group by complex_id
having count(venue_id) > 1;

-- q13 List venues grouped by country
select country_name,
GROUP_CONCAT(distinct venue_name) as venue_names
from venues_table
group by country_name;

-- q14 Find all venues foa a speciifc complex
select ct.complex_name, group_concat(venue_name)
from complexes_table ct join venues_table vt
on ct.complex_id = vt.complex_id
group by complex_name;

-- q15 Get all the competitors with their rank and points
select ct.name, rt.competitor_rank, rt.points
from competitors_table as ct join competitor_rankings_table as rt
on ct.competitor_id = rt.competitor_id;

-- q16 find the competitors in the top5
select ct.name as competitor_names, rt.competitor_rank
from competitors_table as ct join competitor_rankings_table as rt
on ct.competitor_id = rt.competitor_id
order by competitor_rank limit 5;

-- q17 List the competitors with no rank movement
select ct.name as competitor_names, rt.movement
from competitors_table as ct join competitor_rankings_table as rt
on ct.competitor_id = rt.competitor_id
where movement = 0;

-- q18 Get total points of competitors for a specific country
select ct.country, sum(rt.points) as total_points_of_competitors
from competitors_table as ct join competitor_rankings_table as rt
on ct.competitor_id = rt.competitor_id
group by country;

-- q19 Count the no of competitors per country
select country,count(competitor_id) as no_of_competitors
from competitors_table
group by country;

-- q20 Find the competitors with highest points in a current week
select ct.name,rt.points
from competitors_table as ct join competitor_rankings_table as rt
on ct.competitor_id  = rt.competitor_id
order by rt.points desc limit 5;