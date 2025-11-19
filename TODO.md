# TODO for v1.3.0 Deployment and Monitoring

## Deployment
- [ ] Initialize git repository
- [ ] Add all project files to git
- [ ] Commit changes with message "Prepare for v1.3.0 deployment"
- [ ] Install Heroku CLI
- [ ] Login to Heroku
- [ ] Create Heroku app named "instana-apm-dashboard"
- [ ] Set environment variables: DASH_USERNAME=admin, DASH_PASSWORD=securepassword, SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
- [ ] Add Heroku remote
- [ ] Push code to Heroku
- [ ] Scale web dyno to 1
- [ ] Open Heroku app to verify deployment

## Monitoring in Production
- [ ] Add Heroku scheduler addon
- [ ] Schedule data generation: python scripts/generate_instana_all.py --seed 42 --entities 120 --apps 15 --services 40 --issues 30 every hour
- [ ] Verify logs update in real time (check Heroku logs)
- [ ] Confirm alerts are sent (test with sample data)
- [ ] Validate alert thresholds under load

## Feedback & Iteration
- [ ] Share live dashboard URL with teammates
- [ ] Gather usability feedback on navigation, chart clarity, alert usefulness
- [ ] Track issues in GitHub repository

## Portfolio & LinkedIn Update
- [ ] Post v1.3.0 announcement on LinkedIn using drafted post
- [ ] Update portfolio with v1.3.0 milestone
