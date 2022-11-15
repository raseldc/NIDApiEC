Edit at /ets/hosts
192.168.66.2 prportal.nidw.gov.bd
To Gunicorn

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

https://www.codewithharry.com/blogpost/django-deploy-nginx-gunicorn/

python3 -m venv ecnidenv
source ecnidenv/bin/activate

pip install wheel
pip install gunicorn flask

source ecnidenv/bin/activate


export JAVA_OPTS=”-Xms4092m -Xmx4092m”
export JAVA_OPTS=”-Xms2048m -Xmx4092m”

127.0.1.1 app-02.novalocal app-02


systemctl restart haproxy


spring.url=http://172.16.214.27:5001/api/nid/

sudo kill -9 `sudo lsof -t -i:5001`
source ecnidenv/bin/activate
python3 app.py


max_connections = 500

max_user_connections = 500


include proxy_params;
        proxy_pass http://unix:/root/ECNid/gunicorn.sock;

systemctl stop haproxy
sudo systemctl start ecnidgunicorn.socket
sudo systemctl enable ecnidgunicorn.socket
file name: EasyOcr14
server {
    listen 5000;
    server_name "";
	
	location / {
       	include proxy_params;
        proxy_pass http://unix:/root/ocr/EasyOCR14/EasyOCR14.sock;
    }
}
server {
    listen 5001;
    server_name "";
	
	location / {
       	include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}


SELECT DAY(a.creation_date),HOUR(a.creation_date),COUNT(1) FROM icvgd.applicant a 
WHERE a.fiscal_year_id = 4 AND a.creation_date >='2022-11-13' AND (a.app_id_ek_sheba not LIKE '%.%' or a.app_id_ek_sheba IS  NULL )
GROUP BY DAY(a.creation_date),HOUR(a.creation_date);

SELECT DAY(a.creation_date),HOUR(a.creation_date),COUNT(1) FROM icvgd.applicant a 
WHERE a.fiscal_year_id = 4 AND a.creation_date >='2022-11-13' AND (a.app_id_ek_sheba not LIKE '%.%' and a.app_id_ek_sheba IS not NULL )
GROUP BY DAY(a.creation_date),HOUR(a.creation_date);









INSERT INTO application_entry_history(nid,applicant_id_prev,beneficiary_id)
SELECT a.nid, a.id applicant_id_prev,b.id beneficiary_id FROM applicant a 
left JOIN  beneficiary b ON b.nid = a.nid
WHERE a.fiscal_year_id = 3 ;



update application_entry_history 
JOIN (SELECT a.nid nid,a.Id currentId FROM applicant a WHERE a.fiscal_year_id = 4) a
 ON a.nid = application_entry_history.nid

SET application_entry_history.applicant_id_current = a.currentId;

	 INSERT INTO application_entry_history(nid,applicant_id_current)
SELECT applicant.nid,applicant.id
from applicant
where applicant.fiscal_year_id = 4 and
applicant.id not IN ( 
		select a.id from 
		(select a.id,a.nid from applicant a where a.fiscal_year_id=4) a 
 		join application_entry_history on a.nid = application_entry_history.nid
	 );





Data base Table Status

SHOW OPEN TABLES WHERE  `Database` LIKE 'icvgd' AND In_use > 0;
show variables like 'innodb_buffer_pool_size%';