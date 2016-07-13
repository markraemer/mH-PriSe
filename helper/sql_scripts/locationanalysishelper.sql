delete from urls;
delete from location;
INSERT INTO location SET country_code='US', state='California', city='Mountain View', zip_code='94043', log='37.4192', lat='-122.0574' on duplicate key update country_code='US', state='update', city='Mountain View', zip_code='94043', log='37.4192', lat='-122.0574' ;
SELECT count(*) FROM mhealth_apps.location;

INSERT INTO location SET country_code='CN', state='Guangdong', city='Guangzhou', log='23.1167', lat='113.2500' on duplicate key update country_code='CN', state='Guangdong', city='Guangzhou', log='23.1167', lat='113.2500' ;
INSERT INTO urls SET package='com.veclink.movnow.healthy_q2', url='http://120.132.176.172/data2', host='120.132.176.172', analysis='d', time='2016-07-08 11:03:14', test_case='ssl_mitm_forg', location='0' on duplicate key update package='com.veclink.movnow.healthy_q2', url='http://120.132.176.172/data2', host='120.132.176.172', analysis='d', time='2016-07-08 11:03:14', test_case='ssl_mitm_forg', location='0' ;

insert into experiments_details set experiment = (select 16 from experiments limit 1), test_step='pwd_change_freq';

select * from experiments;