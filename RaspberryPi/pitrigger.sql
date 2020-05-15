CREATE TRIGGER reservation_status_update
AFTER INSERT 
ON Spot_Availability
FOR EACH ROW 
BEGIN
    -- IF 5 <= ( SELECT COUNT( /* DISTINCT */ user_id) 
    --           FROM tbl_map_race
    --           WHERE race_id = NEW.race_id)
    -- THEN 
    --     UPDATE tbl_race 
    --     SET race_status = 'Full'
    --       , record_status = '2' 
    --     WHERE race_id = NEW.race_id; 
    -- END IF; 
END