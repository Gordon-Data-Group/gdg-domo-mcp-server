# Elevation

### Get OTP Elevation Setting
`GET {{instanceUrl}}/api/customer/v1/properties/authentication.otp_elevation`

### Authenticate with OTP
`PUT {{instanceUrl}}/api/identity/v1/authentication/elevations/:userId`
- Path: `:userId`
- Body: `{"timeBasedOneTimePassword":"000000"}`

### Update OTP Elevation Setting
`PUT {{instanceUrl}}/api/customer/v1/properties/authentication.otp_elevation`
- Body: `{"value":"false"}`
