# Business Processes Management System (bpms)

It is a backend service for BPMS.

## Work in progress 😄

At this moment the codebase contain some problems, few of them are:
* It should not contain HTML/JS/CSS, but it does
* Token authorization (it's better to be an JWT)
* Some security flaws, such as: user A can delete user B's object
* Not completely DRY
* There is no tests (it is really bad!)

# Rationale

This project is part of BPMS, which was a big project to replace a paid copy of a similar system in my previous job.
The first version was written entirely in Django, no REST, and it was a monolithic service, but I can't tell much about it because of the RND.
After leaving my previous job, I continue to develop BPMS for educational purposes and for people who may be interested in such a project 😊