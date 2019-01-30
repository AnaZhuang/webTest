
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[Users](
	[userId] [bigint] IDENTITY(1,1) NOT NULL,
	[userName] [varchar](50) NULL,
	[password] [varchar](50) NULL
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

insert into Users(userName,password)values('aaaa','123456')
GO
insert into Users(userName,password)values('bbbb','123456')