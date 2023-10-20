# Pulumi Bitbucket Cloud Resource Provider

The Pulumi Bitbucket Cloud Resource Provider lets you manage [Bitbucket](https://bitbucket.org/product) resources.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @pulumi/bitbucket
```

or `yarn`:

```bash
yarn add @pulumi/bitbucket
```

### Python

To use from Python, install using `pip`:

```bash
pip install pulumi_bitbucket
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/ryan-pip/pulumi-bitbucket/sdk/go/...
```

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package Pulumi.Bitbucket
```

## Configuration

The following configuration points are available for the `bitbucket` provider:

- `bitbucket:username` (environment: `BITBUCKET_USERNAME`) - (Optional) Username to use for authentication via Basic Auth.
- `bitbucket:password` (environment: `BITBUCKET_PASSWORD`) - (Optional) Password to use for authentication via Basic Auth
- `bitbucket:oauth_client_id` (environment: `BITBUCKET_OAUTH_CLIENT_ID`) - (Optional) OAuth client ID to use for authentication via Client Credentials Grant. If configured, requires oauth_client_secret to be configured as well.
- `bitbucket:oauth_client_secret` (environment: `BITBUCKET_OAUTH_CLIENT_SECRET`) - (Optional) OAuth client secret to use for authentication via Client Credentials Grant. If configured, requires oauth_client_id to be configured as well.
- `bitbucket:oauth_token` (environment: `BITBUCKET_OAUTH_TOKEN`) - (Optional) An OAuth access token to use for authentication via OAuth. 

## Reference

For detailed reference documentation, please visit [the github repo](https://github.com/ryan-pip/pulumi-bitbucket).
