#import necessary libraries
library(tumblR)
library(wordcloud)

#register api key
api_key<-"XFciVNZ7opOYW9llFIeDzumNCuNEM48mz6Tmq7awI01pHS7SO5"

#call api function once to start the loop
data<-c()
temp_data<-tagged(api_key = api_key, tag="ISIS")
data<-temp_data$response
min<-temp_data$response[[length(temp_data$response)]]$timestamp
size=length(data)

#collect 50000 posts
while (size<=50000){
  
temp_data <- tagged(api_key = api_key, tag='ISIS',before=as.integer(min))
min<-temp_data$response[[length(temp_data$response)]]$timestamp
data<-c(data,temp_data$response)
size=length(data)

}

data<-unique(data)

#remove empty lines
flag<-c()
for (i in 1:length(data)){
  
  if (data[[i]]$summary==""){
    
    flag<-c(flag,i)
  }
  
}

data<-data[-c(flag)]
tagslen<-c()

#initialise matrices to store content
type<-matrix(nrow=length(data),ncol=1)
id<-matrix(nrow=length(data),ncol=1)
date<-matrix(nrow=length(data),ncol=1)
format<-matrix(nrow=length(data),ncol=1)
tags<-c()
dates<-c()
summary<-matrix(nrow=length(data),ncol=1)

#store content in matrices
for (i in 1:length(data)){
  
  type[i]<-data[[i]]$type
  id[i]<-data[[i]]$id
  date[i]<-data[[i]]$date
  summary[i]<-data[[i]]$summary
  format[i]<-data[[i]]$format
  tags<-c(tags,data[[i]]$tags)
  dates<-c(dates,substr(date[[i]],1,4))

}

#write data to a csv
final<-cbind(id,date,type,format,summary)
final<-data.frame(final)
colnames(final)<-c('id','date','type','format','summary')

write.table(final,file='Tumblr.csv',sep=";", row.names = FALSE)

#get unique counts to plot data
counts_type<-table(type)
counts_tags<-table(tags)
counts_format<-table(format)
counts_dates<-table(dates)

for_bar1<-c()
for_bar2<-c()
for_bar3<-c()
for_bar4<-c()
for_bar1<-c(for_bar1,(counts_tags['ISIS']+counts_tags['Isis']+counts_tags['isis']))
for_bar2<-c(for_bar2,(counts_tags['IS']+counts_tags['Is']+counts_tags['is']))
for_bar3<-c(for_bar3,(counts_tags['ISLAMIC STATE']+counts_tags['Islamic State']+counts_tags['islamic state']))
for_bar4<-c(for_bar4,(counts_tags['ISIL']+counts_tags['Isil']+counts_tags['isil']))

#plot data
xx<-barplot(c(for_bar4,for_bar2,for_bar1,for_bar3),main='Tags Distribution',xlab='Tags',ylab='Frequency',col='darkblue',ylim=c(0,40000))
text(x=xx,y=c(10128,5341,35076,9643),labels=c(10128,5341,35076,9643),pos=3,cex = 0.8, col = "red")

yy<-barplot(counts_type[c(1,4,5,2,3)],main='Post Type Distribution',xlab='Post Type',ylab='Frequency',col='darkblue',ylim=c(0,25000))
text(x=yy,y=c(103,6543,18197,522,303),labels=c(103,6543,18197,522,303),pos=3,cex = 0.8, col = "red")

zz<-barplot(counts_dates[c(6:12)],main='Post per Year',xlab='Year',ylab='Frequency',col='darkblue',ylim=c(0,21000))
text(x=zz,y=c(1579,2889,4301,16290,10661,5927,7591),labels=c(1579,2889,4301,16290,10661,5927,7591),pos=3,cex = 0.8, col = "red")
