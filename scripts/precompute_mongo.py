# scripts/precompute_mongo.py – Q1-Q15, Kayfa_database
import pandas as pd
import numpy as np
import json, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"

def load(name): return pd.read_csv(DATA / f"{name}_cleaned.csv")

students = load('students')
groups = load('groups')
courses = load('courses')
grades = load('grades')
attendance = load('attendance')
eng = load('engagement_events')
concepts = load('concepts_performance')
assub = load('assignment_submissions')

concepts.loc[(concepts['score_pct'] == 60) & (concepts['mastery_status'].str.lower() == 'failed'), 'mastery_status'] = 'passed'

out_dir = BASE / "scripts" / "seed_json"
out_dir.mkdir(exist_ok=True, parents=True)
def save(name, obj):
    with open(out_dir / f"{name}.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, default=str)

# Q1
attendance['present'] = attendance['status'].str.lower() == 'attended'
group_att = attendance.groupby('group_id')['present'].mean().reset_index()
group_att['attendance_rate'] = (group_att['present']*100).round(1)
group_att = group_att.merge(groups[['group_id','group_name','course_id','instructor']], on='group_id')
platform_avg = group_att['attendance_rate'].mean()
group_att['status_label'] = np.where(group_att['attendance_rate'] < platform_avg, 'Below average', 'Above average')
save('q1_attendance', group_att.to_dict('records'))
save('q1_meta', {'platform_avg': round(platform_avg,2)})

# Q2
grades['score_pct'] = grades['score'] / grades['max_score'] * 100
summary = grades.groupby('type')['score_pct'].agg(['count','mean','median','std','min','max']).reset_index()
summary['cv'] = summary['std'] / summary['mean']
save('q2_assessment_type', summary.round(2).to_dict('records'))
save('q2_distribution', grades[['type','score_pct']].to_dict('records'))

# Q3
course_stats = grades.groupby('course_id')['score_pct'].agg(['count','mean','median','std']).reset_index()
course_stats = course_stats.merge(courses[['course_id','course_name']], on='course_id')
save('q3_course_grades', course_stats.round(2).to_dict('records'))
save('q3_distribution', grades.merge(courses[['course_id','course_name']], on='course_id')[['course_name','score_pct']].to_dict('records'))

# Q4
att_student = attendance.groupby('student_id')['present'].mean().reset_index()
att_student['attendance_rate'] = att_student['present']*100
grade_student = grades.groupby('student_id')['score_pct'].mean().reset_index(name='avg_grade')
q4 = att_student[['student_id','attendance_rate']].merge(grade_student, on='student_id')
r = q4['attendance_rate'].corr(q4['avg_grade'])
save('q4_attendance_grade', {'r': round(r,3), 'points': q4.to_dict('records')})

# Q5
login_freq = eng[eng['event_type']=='login'].groupby('student_id').size().rename('login_frequency')
video_time = eng[eng['event_type']=='video_watch'].groupby('student_id')['duration_seconds'].sum().rename('video_watch_time_sec')
eng_student = pd.concat([login_freq, video_time], axis=1).fillna(0).reset_index()
eng_student['video_watch_hours'] = eng_student['video_watch_time_sec']/3600
q5 = eng_student.merge(grade_student, on='student_id', how='inner')
corr = q5[['login_frequency','video_watch_hours','avg_grade']].corr().round(3)
save('q5_engagement', {'corr': corr.to_dict(), 'points': q5.to_dict('records')})

# Q6
concepts['failed'] = concepts['mastery_status'].str.lower() == 'failed'
stats = concepts.groupby(['course_id','concept_name'], as_index=False)['failed'].agg(n='count', fails='sum', fail_rate='mean')
stats['fail_rate'] = (stats['fail_rate']*100).round(2)
stats = stats.merge(courses[['course_id','course_name']], on='course_id').sort_values('fail_rate', ascending=False)
save('q6_concepts', stats.head(20).to_dict('records'))

# Q7
rec = concepts[(concepts['course_id']=='C002') & (concepts['concept_name']=='Recursion')].copy()
rec['mastered'] = rec['mastery_status'].str.lower() == 'passed'
assess = rec.groupby('assessment_id').agg(n=('mastered','count'), mastered=('mastered','sum'), mean_score=('score_pct','mean')).reset_index()
assess['mastery_rate'] = assess['mastered']/assess['n']*100
save('q7_recursion_mastery', assess.to_dict('records'))

# Q8
grade_agg = grades.groupby(['student_id','course_id','assessment_id'], as_index=False)['score_pct'].mean().rename(columns={'score_pct':'grade_pct'})
merged = assub.merge(grade_agg, on=['student_id','course_id','assessment_id'], how='left')
merged['deadline'] = pd.to_datetime(merged['deadline'], errors='coerce')
merged['submitted_at'] = pd.to_datetime(merged['submitted_at'], errors='coerce')
merged['buffer_hours'] = (merged['deadline'] - merged['submitted_at']).dt.total_seconds()/3600
bins = [-np.inf, 0, 6, 24, 72, np.inf]
labels = ['Late', '0-6h early', '6-24h early', '1-3d early', '3d+ early']
merged['buffer_bin'] = pd.cut(merged['buffer_hours'], bins=bins, labels=labels)
bin_stats = merged.groupby('buffer_bin', observed=True)['grade_pct'].mean().reset_index()
save('q8_submission_timing', bin_stats.to_dict('records'))

# Q9
attendance['session_datetime'] = pd.to_datetime(attendance['session_datetime'], errors='coerce')
eng['event_datetime'] = pd.to_datetime(eng['event_datetime'], errors='coerce')
att_weekly = attendance.set_index('session_datetime').resample('W')['present'].agg(['count','mean']).reset_index()
att_weekly['attendance_rate'] = att_weekly['mean']*100
eng_weekly = eng.set_index('event_datetime').resample('W').size().reset_index(name='events')
ts = pd.merge(att_weekly[['session_datetime','attendance_rate']], eng_weekly, left_on='session_datetime', right_on='event_datetime', how='outer')
ts['session_datetime'] = ts['session_datetime'].astype(str)
save('q9_term_trends', ts[['session_datetime','attendance_rate','events']].dropna().to_dict('records'))

# Q10
grade_s = grades.groupby('student_id')['score_pct'].mean().rename('avg_grade')
att_s = attendance.groupby('student_id')['present'].mean().rename('attendance_rate') * 100
eng_s = eng.groupby('student_id').size().rename('engagement_count')
metrics = students[['student_id','age']].set_index('student_id').join([grade_s, att_s, eng_s])
metrics['engagement_count'] = metrics['engagement_count'].fillna(0)
def age_band(a):
    if pd.isna(a) or a==0: return 'Unknown'
    if a < 20: return '18-19'
    if a <= 22: return '20-22'
    if a <= 25: return '23-25'
    return '26+'
metrics['age_band'] = metrics['age'].apply(age_band)
summary = metrics.groupby('age_band').agg(n_students=('age','count'), avg_grade=('avg_grade','mean'), attendance_rate=('attendance_rate','mean'), engagement_count=('engagement_count','mean')).reset_index()
save('q10_age_bands', summary.round(2).to_dict('records'))

# Q11
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
att_rate_q11 = attendance.groupby('student_id')['present'].mean().rename('attendance_rate')
eng_events_q11 = eng.groupby('student_id').size().rename('engagement_events')
grade_avg_q11 = grades.groupby('student_id')['score_pct'].mean().rename('avg_grade')
failed_concepts_q11 = concepts.groupby('student_id')['failed'].sum().rename('failed_concepts')
seg = pd.concat([att_rate_q11, eng_events_q11, grade_avg_q11, failed_concepts_q11], axis=1).fillna(0)
X = StandardScaler().fit_transform(seg[['attendance_rate','engagement_events','avg_grade','failed_concepts']])
seg['cluster'] = KMeans(n_clusters=4, random_state=42, n_init=20).fit_predict(X)
names = {0:'High Achievers',1:'Disengaged At-Risk',2:'Steady Performers',3:'Struggling Attenders'}
seg['segment'] = seg['cluster'].map(names)
seg_reset = seg.reset_index()
save('q11_segments', seg_reset[['student_id','attendance_rate','engagement_events','avg_grade','failed_concepts','segment']].to_dict('records'))

# Q12
true_counts = students['group_id'].value_counts()
merged12 = groups.merge(true_counts.rename('true_count'), left_on='group_id', right_index=True, how='left')
merged12['true_count'] = merged12['true_count'].fillna(0).astype(int)
merged12['discrepancy'] = merged12['true_count'] - merged12['stated_num_students']
save('q12_group_sizes', merged12[['group_id','group_name','stated_num_students','true_count','discrepancy']].to_dict('records'))

# Q13
save('q13_merge_recommendation', {
    'small_group': 'G10', 'size': 1,
    'closest_student_match': {'g10_student': 'S0500', 'target_student': 'S0397', 'target_group': 'G08'},
    'centroid_closest_group': 'G08',
    'recommendation': 'Merge G10 into G08 – concept profile closest, preserves cohort balance.'
})

# --- Q14 – FIXED: recompute all features with consistent names ---
att_rate = attendance.groupby('student_id')['present'].mean().rename('attendance_rate')
eng_count = eng.groupby('student_id').size().rename('engagement_count')
eng['event_datetime'] = pd.to_datetime(eng['event_datetime'], errors='coerce')
def engagement_decline(sdf):
    if len(sdf) < 4: return 0.0
    sdf = sdf.sort_values('event_datetime')
    mid = sdf['event_datetime'].quantile(0.5)
    early = (sdf['event_datetime'] <= mid).sum()
    late = (sdf['event_datetime'] > mid).sum()
    return max(0, (early - late) / early) if early else 0.0
decline = eng.groupby('student_id').apply(engagement_decline, include_groups=False).rename('engagement_decline')
fail_rates = concepts.groupby('concept_id')['failed'].mean()
key_concepts = fail_rates[fail_rates > 0.40].index.tolist()
concepts['is_key'] = concepts['concept_id'].isin(key_concepts)
failed_key = concepts[concepts['is_key']].groupby('student_id')['failed'].sum().rename('failed_key_concepts')
failed_all = concepts.groupby('student_id')['failed'].sum().rename('failed_concepts')
grade_avg2 = grades.groupby('student_id')['score_pct'].mean().rename('avg_grade')
base = students.set_index('student_id')[['full_name','group_id']]
risk = base.join([att_rate, eng_count, decline, failed_key, failed_all, grade_avg2]).fillna(0)
def minmax(s): return (s - s.min()) / (s.max() - s.min() + 1e-9)
risk['attendance_risk'] = 1 - risk['attendance_rate']
risk['eng_decline_risk'] = risk['engagement_decline'].clip(0,1)
risk['eng_volume_risk'] = 1 - minmax(risk['engagement_count'])
risk['key_fail_risk'] = minmax(risk['failed_key_concepts'])
risk['at_risk_score'] = 0.35*risk['attendance_risk'] + 0.25*risk['eng_decline_risk'] + 0.15*risk['eng_volume_risk'] + 0.25*risk['key_fail_risk']
top10 = risk.sort_values('at_risk_score', ascending=False).head(10).reset_index()
save('q14_at_risk', top10[['student_id','full_name','group_id','attendance_rate','engagement_count','failed_key_concepts','avg_grade','at_risk_score']].round(3).to_dict('records'))

# Q15
grades['date'] = pd.to_datetime(grades['date'], errors='coerce')
assess_order = grades.groupby(['course_id','assessment_title','type'], as_index=False)['date'].min()
assess_order = assess_order.sort_values(['course_id','date'])
assess_order['assessment_seq'] = assess_order.groupby('course_id').cumcount() + 1
grades2 = grades.merge(assess_order[['course_id','assessment_title','type','assessment_seq']], on=['course_id','assessment_title','type'], how='left')
group_assess = grades2.groupby(['course_id','group_id','assessment_seq','assessment_title'], as_index=False)['score'].mean()
group_assess.rename(columns={'score':'avg_score'}, inplace=True)
trends = []
for gid, df in group_assess.groupby('group_id'):
    df = df.sort_values('assessment_seq')
    slope = np.polyfit(df['assessment_seq'], df['avg_score'], 1)[0]
    trends.append({'group_id': gid, 'slope': round(float(slope),2), 'first': round(float(df['avg_score'].iloc[0]),1), 'last': round(float(df['avg_score'].iloc[-1]),1)})
save('q15_group_trends', trends)
save('q15_group_assess', group_assess.round(1).to_dict('records'))

print("All Q1-Q15 exported to scripts/seed_json/")

# MongoDB upload
MONGO_URI = os.getenv("MONGO_URI", "")
if MONGO_URI:
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI)
    db_name = os.getenv("MONGO_DB", "Kayfa_database")
    db = client[db_name]
    import json
    for f in (Path(__file__).parent / "seed_json").glob("q*.json"):
        coll = f.stem
        with open(f) as jf:
            data = json.load(jf)
        db[coll].delete_many({})
        if isinstance(data, list):
            if data: db[coll].insert_many(data)
        else:
            db[coll].insert_one(data)
        print(f" {coll}: {len(data) if isinstance(data, list) else 1} docs")
    print(f"Uploaded to {db_name}")