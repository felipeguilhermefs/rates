package main

import (
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	router.GET("/rates", ratesHandler(0))
	router.GET("/rates_null", ratesHandler(3))
	router.POST("/prices", pricesHandler)

	router.Run()
	// router.Run(":3000") // or some configured port
}

// PeriodQueryParam wrap period data from requests
type PeriodQueryParam struct {
	From time.Time `form:"date_from" binding:"required" time_format:"2006-01-02"`
	To   time.Time `form:"date_to" binding:"required" time_format:"2006-01-02"`
}

// RouteQueryParam wrap port/region data from requests
// PORT_PATTERN = re.compile(r'^[A-Z]{5}$')
// REGION_PATTERN = re.compile(r'^\w+$')
type RouteQueryParam struct {
	Origin      string `form:"origin" binding:"required"`
	Destination string `form:"destination" binding:"required"`
}

func ratesHandler(minSample int) func(c *gin.Context) {
	return func(c *gin.Context) {
		var period PeriodQueryParam
		if err := c.ShouldBindQuery(&period); err != nil {
			c.JSON(400, gin.H{"error": err.Error()})
			return
		}

		var route RouteQueryParam
		if err := c.ShouldBindQuery(&route); err != nil {
			c.JSON(400, gin.H{"error": err.Error()})
			return
		}

		c.JSON(200, gin.H{
			"message":     "rates" + string(minSample),
			"from":        period.From,
			"to":          period.To,
			"origin":      route.Origin,
			"destination": route.Destination,
		})
	}
}

func pricesHandler(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "prices",
	})
}
