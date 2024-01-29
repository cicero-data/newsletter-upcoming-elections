WITH next_elections AS (
  SELECT eec.chamber_id, ee.election_expire_date as edate, ee.remarks, ee.url_1,
  ee.id, ee.is_by_election as special, ee.is_runoff_election as runoff
  FROM webservice_electionevent ee
  LEFT JOIN webservice_electionevent_chambers eec
    ON ee.id = eec.electionevent_id
  INNER JOIN webservice_chamber c ON eec.chamber_id = c.id
  INNER JOIN webservice_government g ON c.government_id = g.id
  WHERE ee.trans_to IS null AND ee.election_expire_date > now() 
  AND ((ee.is_general_election AND ee.officials_are_elected)
     OR ((ee.is_primary_election AND ee.officials_are_elected)))
  AND NOT (ee.is_by_election OR ee.is_runoff_election OR ee.is_referendum)
  AND NOT ( (ee.is_local OR ee.is_state) AND g.type='NATIONAL')
  GROUP BY ee.election_expire_date, eec.chamber_id, ee.remarks, ee.url_1, ee.id
),
chambers_with_officials AS (
  SELECT c.id, c.sk, c.name_formal, g.state, g.type as gov_type, s.fips as country_code, 
  c.official_count,  c.term_length, c.url, c.election_frequency
  FROM webservice_chamber c
  LEFT JOIN webservice_official o ON c.id = o.chamber_id
  INNER JOIN webservice_government g ON c.government_id = g.id
  INNER JOIN webservice_country s ON g.country_id = s.id
  WHERE o.trans_to IS null AND o.valid_to > now() AND c.trans_to IS null
  AND NOT c.is_appointed
  GROUP BY c.id, c.sk, c.name_formal, g.state, gov_type, country_code, c.term_length
)
SELECT 
c.id, c.sk, c.name_formal, state, gov_type, country_code, c.official_count, c.term_length, c.url,
ne.upcoming_election, ne.remarks as ue_remarks, ne.url_1 as ue_url_1,
ne.special, ne.runoff
FROM chambers_with_officials c

LEFT JOIN 
(SELECT DISTINCT ON (chamber_id) chamber_id, edate AS upcoming_election, remarks, url_1, id, special, runoff
    FROM next_elections
    ORDER BY chamber_id, edate ASC NULLS LAST, remarks, url_1, id) ne
ON c.id = ne.chamber_id