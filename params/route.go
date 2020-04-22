package params

// Route holds origin and destination params used in the API's
type Route struct {
	Origin      string `form:"origin" json:"origin" binding:"required"`
	Destination string `form:"destination" json:"destination" binding:"required"`
}
