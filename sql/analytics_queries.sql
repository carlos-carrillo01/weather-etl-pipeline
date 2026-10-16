-- Average maximum temperature per day

SELECT 
    date,
    ROUND(AVG(temp_max_c)::numeric, 1) AS avg_temp_max_c
FROM weather
GROUP BY date
ORDER BY date;

-- Day with more precipitation

SELECT 
    date,
    precipitation_mm
FROM weather
ORDER BY precipitation_mm DESC
LIMIT 1;

-- Daily thermal range

SELECT 
    date,
    temp_max_c,
    temp_min_c,
    ROUND((temp_max_c - temp_min_c)::numeric, 1) AS temp_range_c
FROM weather
ORDER BY temp_range_c DESC;
