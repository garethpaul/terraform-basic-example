mock_provider "aws" {}

run "accept_default_resource_tags" {
  command = plan
}

run "accept_resource_tag_length_boundaries" {
  command = plan

  variables {
    resource_tags = {
      (join("", [for index in range(128) : "k"])) = join("", [for index in range(256) : "v"])
    }
  }
}

run "accept_49_resource_tags_without_name" {
  command = plan

  variables {
    resource_tags = {
      for index in range(49) : "Tag${index}" => "terraform"
    }
  }
}

run "accept_50_resource_tags_with_name" {
  command = plan

  variables {
    resource_tags = merge(
      {
        Name = "caller-value"
      },
      {
        for index in range(49) : "Tag${index}" => "terraform"
      }
    )
  }
}

run "reject_empty_resource_tags" {
  command = plan

  variables {
    resource_tags = {}
  }

  expect_failures = [var.resource_tags]
}

run "reject_blank_resource_tag_key" {
  command = plan

  variables {
    resource_tags = {
      " " = "terraform"
    }
  }

  expect_failures = [var.resource_tags]
}

run "reject_blank_resource_tag_value" {
  command = plan

  variables {
    resource_tags = {
      Owner = " "
    }
  }

  expect_failures = [var.resource_tags]
}

run "reject_reserved_resource_tag_key" {
  command = plan

  variables {
    resource_tags = {
      "aws:owner" = "platform"
    }
  }

  expect_failures = [var.resource_tags]
}

run "reject_overlong_resource_tag_key" {
  command = plan

  variables {
    resource_tags = {
      (join("", [for index in range(129) : "k"])) = "terraform"
    }
  }

  expect_failures = [var.resource_tags]
}

run "reject_overlong_resource_tag_value" {
  command = plan

  variables {
    resource_tags = {
      Owner = join("", [for index in range(257) : "v"])
    }
  }

  expect_failures = [var.resource_tags]
}

run "reject_50_resource_tags_without_name" {
  command = plan

  variables {
    resource_tags = {
      for index in range(50) : "Tag${index}" => "terraform"
    }
  }

  expect_failures = [var.resource_tags]
}
