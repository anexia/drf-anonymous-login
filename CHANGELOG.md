# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0 - Unreleased]

### Added
- Support for Python 3.12 and 3.13
- Support for Django 5.0 and 5.1
- Mixin for User to provide properties `is_anonymous_login` and `anonymous_login`
- Cookie authentication support

### Changed
- pre-commit configuration

### Removed
- Support for Python 3.8
- Support for Django 3.2 and 4.1

## [1.1.0]

### Added
- settings.ANONYMOUS_LOGIN_EXPIRATION to allow expiration of AnonymousLogin

## [1.0.0]

### Added
- Initial setup

[Unreleased]: https://github.com/anexia/drf-anonymous-login/compare/1.0.0...HEAD
[1.0.0]: https://github.com/anexia/drf-anonymous-login/releases/tag/1.0.0
