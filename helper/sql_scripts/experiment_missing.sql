select tc.name, group_concat(ts.name) from experiment_test_steps ts join experiment_test_cases tc on ts.test_case = tc.name group by tc.name; 

select a.package, b.test_case, b.test_steps, b.num from apps a, (select tc.name as test_case, group_concat(ts.name separator '\n') as test_steps, count(ts.name) as num from experiment_test_steps ts join experiment_test_cases tc on ts.test_case = tc.name 
where ts.name not in (select test_step from experiments_details ed join experiments e on ed.experiment = e.id where 
e.package=a.package)  group by tc.name) b;

select tc.name as test_case, group_concat(ts.name) as test_steps, count(ts.name) as num from experiment_test_steps ts join experiment_test_cases tc on ts.test_case = tc.name 
where ts.name not in (select test_step from experiments_details ed join experiments e on ed.experiment = e.id where 
e.package='com.withings.wiscale2')  group by tc.name;