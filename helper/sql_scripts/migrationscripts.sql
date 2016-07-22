select * from experiments where test_case = 'user_registration';

select * from experiments_details where test_step in (select name from experiment_test_steps where test_case = 'user_registration');

#delete from experiment_test_steps where test_case = 'av3_mobile_app';

select concat( 'av3_', `name` ) as `name`, `order`, 'av3_mobile_app', short_desc, rating, long_desc from experiment_test_steps;

insert into experiment_test_steps (select concat( 'av3_', `name` ) as `name`, `order`, 'av3_mobile_app', short_desc, rating, long_desc from experiment_test_steps where test_case='user_registration');


insert into experiments (package, time, test_case, comment, log_folder) select package, time, 'av3_mobile_app', 'aggregated from teststeps', replace(log_folder,'user_registration','av3_mobile_app') from experiments where test_case='user_registration';

insert into experiments_details (experiment, test_step, comment) select experiment, 'av3_reg_data_input', comment from experiments_details where test_step = 'reg_data_input' ;

select * from experiments where test_case='data_com';

delete from experiments where test_case='ssl_mitm_forg';

insert into experiments_details (experiment, test_step, comment) select (select n.id from experiments n where n.package = o.package and n.test_case = 'data_com') as experiment, 'data_com_ssl_forg' as test_step, o.comment as comment  from experiments o where test_case='ssl_mitm_forg';