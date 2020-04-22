package params

import "time"

// Period holds time period params used in the API's
type Period struct {
	From time.Time `form:"date_from" json:"date_from" binding:"required" time_format:"2006-01-02"`
	To   time.Time `form:"date_to" json:"date_to" binding:"required,gtefield=From" time_format:"2006-01-02"`
}
